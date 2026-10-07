from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

@login_required
def place_list(request):


    if request.method == 'POST': # Create a place from the submitted form.
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) # Set the owner before saving the place.
        place.user = request.user  
        if form.is_valid():  # Save only valid form data.
            place.save()
            return redirect('place_list') # Refresh the wishlist after saving.

    
    # Show only the current user's unvisited places and add form.
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': form})


@login_required
def places_visited(request):
    # Show the current user's completed trips.
    visited = Place.objects.filter(user=request.user).filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:    # Prevent users changing someone else's place.
            place.visited = True   
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')       # Return to the wishlist.


@login_required
def delete_place(request, place_pk):
    # Let users delete only their own places.
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


@login_required
def about(request):
    # Supply basic site information to the About page.
    author = 'Jake'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})


@login_required
def place_details(request, place_pk):

    place = get_object_or_404(Place, pk=place_pk)

    if place.user != request.user: # Keep trip details private to their owner.
        return HttpResponseForbidden()

    # Save submitted review details for this place.
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)  # Update this existing place.
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)  # Show validation errors once.

        return redirect('place_details', place_pk=place_pk)

    else:    # Display the place details.
        if place.visited:
            review_form = TripReviewForm(instance=place)  # Pre-fill saved trip details.
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form} )

        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place} )

