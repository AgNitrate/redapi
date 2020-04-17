# redapi

This project is based off of whatapi and provides a wrapper around the AJAX API for Redacted.ch. 
As of right now, it only supports API Key authentication. 

## Example usage:

```python
    >>> import redapi
    >>> apihandle = redapi.RedAPI(apikey='v22rdsreb.cg54vt5 3633fyru2894fg54')
    >>> apihandle.request("browse", searchstr="Square Up")
    ...
    >>> apihandle.get_torrent()
```


To use another tracker:

```python

    >>> import redapi
    >>> apihandle = redapi.RedAPI(apikey='v22rdsreb.cg54vt5 3633fyru2894fg54', server='https://passtheheadphones.me')
    >>> apihandle.request("browse", searchstr="The Beatles")
    ...
```


Basic API reference available at  [What documentation](https://github.com/WhatCD/Gazelle/wiki/JSON-API-Documentation) and on the [Redacted API Documentation](https://redacted.ch/wiki.php?action=article&id=455). 
