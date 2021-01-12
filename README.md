# pyloton

This package is a python client for the Peloton API.

## Example Usage
```python
    from pyloton import pyloton
    import time
    
    # insert your peloton_username and peloton_password if you wish to make any credentialed calls
    Pyloton = pyloton.Pyloton(peloton_username, peloton_password)
    registered_classes, live_class_catalog = Pyloton.get_registered_classes()

    for registered_class in registered_classes:
        ride = None
        for _ride in live_class_catalog.rides:
            if _ride.id == registered_class.ride_id:
                ride = _ride

        instructor = None
        for _instructor in live_class_catalog.instructors:
            if _instructor.id == ride.instructor_id:
                instructor = _instructor

        print('Title: ', ride.title)
        print('Instructor: ', instructor.name)
        print('Scheduled Start: ', time.strftime("%d %b %Y %H:%M:%S", time.localtime(registered_class.scheduled_start_time)))
        print('Duration: ', ride.duration / 60)
```