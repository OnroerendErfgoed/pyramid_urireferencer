0.6.0 (2017-06-08)
------------------

- Add some extra logging. (#13)
- Add required function :meth:`get_uri` to the :class:`AbstractReferencer` to determine the uri of the current request (#7 and #8)


0.5.0 (2016-09-28)
------------------

- Add support for python 3.5
- Some minor doc fixes
- Changed an edge case where `items` or `applications` response attributes could
  be `None` so that they are now always empty lists. (#6)
- Updated error message and added JSON error message when a backend application can't be reached (#9) and when a resource can't be deleted (#10)

0.4.0 (2015-07-10)
------------------

- Added module `protected_resources` containing a `protected_operation` decorator function.

0.3.0 (2015-06-25)
------------------

- Added uri and request to references parameters
- Included renderer in request config
- Removed exception in get_references view
- Fixed ApplicationResponse title from json

0.2.0 (2015-06-07)
------------------

- Changed ApplicationResponse.url to service_url.
- Cleaned up some documentation.
- Added an AbstractReferencer that has no implementation whatsoever.
- Added Python Wheel support
- Make sure that the uri parameter is properly urlencoded.


0.1.0 (2015-05-21)
------------------

-  Initial version
