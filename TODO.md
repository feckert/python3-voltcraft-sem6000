# Replace gatttool dependency with gatt-python

- [ ] cleaner API for working with weekdays
- [ ] cleaner API for working with repeated schedulers - no need to provide a date here
- [x] cleaner API for working with timer - rename is_timer_running to is_active 
- [ ] cleaner API response - replace separate values with isotime or isodatetime
- [ ] cleaner API for returning device name - return notification object as response
- [ ] introduce set_timer command for explicit target date and time - for restoring settings
- [ ] rename led command to nightmode
- [ ] cleaner API - use change instead of set consistently
- [x] move pseudo commands from cli demo to sem6000 module (i.e. reset\_timer, reset\_random_mode)
- [ ] introduce hierarchy in settings response (i.e. reduced-perion sub-object)
- [ ] settings backup / restore cli: beautification of JSON
