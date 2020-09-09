# Replace gatttool dependency with gatt-python

- [ ] cleaner API for working with weekdays
- [x] cleaner API for working with timer - rename is_timer_running to is_active 
- [x] cleaner API response - replace separate values with isotime or isodatetime
- [x] cleaner API for schedulers - separate fields for isodate and isotime, since date values can be empty
- [x] cleaner API for returning device name - return notification object as response
- [ ] introduce set_timer command for explicit target date and time - for restoring settings
- [x] rename led command to nightmode
- [ ] cleaner API - use change or set consistently
- [x] move pseudo commands from cli demo to sem6000 module (i.e. reset\_timer, reset\_random_mode)
- [ ] introduce hierarchy in settings response (i.e. reduced-period sub-object)
- [ ] settings backup / restore cli: beautification of JSON
