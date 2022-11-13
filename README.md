<h1 align="center">
  clrprint v2.0
<div align="center">

[![Generic badge](https://img.shields.io/badge/Made_By-ABHIJITH_BOPPE-BLUE.svg)](https://www.linkedin.com/in/abhijith-boppe/)  
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://github.com/AbhijithAJ/clrprint/blob/master/LICENSE) [![PayPal](https://img.shields.io/badge/donate-PayPal-blue.svg)](https://www.paypal.me/abhijithboppes) 
</div>

</h1>
 
 - Port forwarding under various NAT networks using a single line of code/command.
 - Need UPnP to be Enabled on Routers/Gateways.
 - It's wrapper around  [MiniUPnP](http://miniupnp.free.fr/).
 - Works on Linux and Windows.
---
## ABOUT

You can apply a port forwarding rule from your host machine itself with a single command.
To use this application, your router or gateway must have UPnP enabled.

**Usage**

Just download repository and use it from terminal/cmd prompt.

## Command line Usage Examples

**Add port Forward Rule**
```powershell
python upnpPortForward.py add 80 80 tcp
python upnpPortForward.py add 443 8080 tcp
```

**Remove port Forward Rule**
```powershell
python upnpPortForward.py remove 80 tcp
python upnpPortForward.py remove 443 tcp
```

**List port forward rule table**
```powershell
python upnpPortForward.py list
```

## License & copyright
© Abhijith Boppe, Security analyst

<a href="https://linkedin.com/in/abhijith-boppe" target="_blank">LinkedIn</a>

Licensed under the [MIT License](LICENSE)
