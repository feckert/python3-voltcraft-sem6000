# Replace gatttool dependency with gatt-python

- [ ] cleaner API for working with weekdays
- [ ] cleaner API for working with repeated schedulers - no need to provide a date here
- [ ] cleaner API for working with timer - rename is_timer_running to is_active 
- [ ] cleaner API response - separate values with isotime or isodatetime
- [ ] introduce set_timer command for explicit target date and time - for restoring settings
- [ ] rename led command to nightmode
- [ ] cleaner API - use change instead of set consistently
- [ ] move pseudo commands from cli demo to sem6000 module (i.e. reset\_timer)
- [ ] introduce hierarchy in settings response (i.e. reduced-perion sub-object)
- [ ] settings backup / restore cli: beautification of JSON
