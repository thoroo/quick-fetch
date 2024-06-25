# QuickFetch
A python script (mainly for personal use and may not be as applicable to other situations; flexibility has been in mind though) that enables downloading a single file or image from the active web browser tab (using `pywinauto`) when a keyboard button is pressed and downloads using a headless Chrome driver (using `selenium`). Ability to navigate pages using `PyScreeze` image locator.

QuickFetch is a semi-automatic tool that requires user input and is meant to be used to reduce time spent in order to download a file or image when looking at individual items in a page using a grid or lazy loading that are presented on screen.

### Key features

- Saves downloads in a user specified directory
- Downloads an image direct from an image link
- Downloads an image in which one must click on a link to get to image page (e.g. grid of lazy loading images)
- Downloads a file direct from a source link (WIP Currently not implemented)
- Downloads a file in which one must click on a link to get to page with download link (e.g. selecting from a grid of items)
- Can grab metadata (currently only two strings/elements) to use for file naming
- Can unzip files after download
- Can handle buttons on page that requires user input in order to show content on page, i.e. gatekeeping buttons such as age restrictions
- Quick button to move to previous or next page (works by Pyscreeze locating image of button on screen)
- Config selection to setup different settings for different pages
- Adding suffix or prefix to downloaded files
- Clean and colorful console logs
- Sound chimes to indicate whether a download is finished

### ToDo

- Add better exception handling
- Add custom scroller for pages with lazy loading
- Ensuring host name is correct when navigating using next or previous button. In case a website has some sort of redirect URL to a external site
- Maybe implement some sort of asynch functionality to be able to press for next item instead of waiting.
    - Temp folder needs to be reworked in that case
- Add example config for showcasing XPaths
- Add functionality in user other drivers, e.g. IE and Firefox
- Add combined functionality between `grab` and `fetch`
- Add logging to file if that is of interest
- Add custom formatting of metadata strings
- Add grabbing videos from streaming platforms using `youtube-dl`
- Reduce time between input and grabbing the URL from `XPath mode`
- Reduce time between input and grabbing indirectly using `Mouse mode`. Sits currently at roughly 10 seconds (however, no issues regarding user input)

### Current issues

- 5 second lag for `XPath mode´ and an indirect grab, additionally when you change tab or window during this time period it might grab the URL from the changed tab/window
- Checking for downloaded files has a timeout for 120 seconds. If download speed is low or if the file is large enough, it will cut off the download and close the application
- Acronyms that have all capitals are turned into title case
- Rich console shows code when not in administrator mode when using CMD

## Installation

```bash
pip install git+https://github.com/Phiido/quick-fetch
```

- Note that QuickFetch **requires** '>= Python 3.8.0'
- Can currently **only** run on Chrome and its driver

Default config file can be found in project folder './config_files/'. For custom settings, make a copy of
the config file and rename it (for example hostname of the page you want to target), adjust settings for your needs. See below 
for detailed information on config settings.

If you want to use page navigator buttons, create a copy of the button image(s) that are present on screen in the Chrome window, they can be setup anywhere as config reads which paths where they are located.

Setting up XPaths are required, though not all of them depending on usage.

Finding XPaths for an element can be done by going into DevTools (pressing F12 for Chrome), right clicking on the target element and copy the XPath string. A good tutorial can be found at [W3schools](https://www.w3schools.com/xml/xpath_intro.asp) for more advanced search methods. Double check that the XPath is correct by doing a search (CTRL + F) inside the elements tab of DevTools. You should only get a single hit, if it is 0 or >1, rewrite it.

## Usage

```bash
python3 -m quick-fetch
```

- Setting the mode of operation in config: 

    - **Mouse:** Grabs the URL from where the mouse pointer is located. Useful for dealing with images
    - **XPaths:** Moves into either next URL or download link based on configured XPaths. Useful when dealing with files (e.g. zip-files)

- Choosing which config from those that are available in './config_files/.

**Note:** There is some validation of button clicks and copied URLs when using `Mouse mode`, however, Chrome has implemented quick access to *Reading Mode* that will be opened instead when pressing the hotkey for `Direct download` when over a non-link element. A workaround is to disable *Reading Mode* from Chrome flags (<chrome://flags/>).

## Config settings

**Note**: If there are no config files present in './config_files/', QuickFetch will attempt to recreate the default config file.

The config is divided into the following sections:

### General

- Mode: Which mode to use when fetching (possible values are 'Mouse' and 'XPath'); Defaults to 'Mouse'
- Unzip: Whether to unzip downloaded zip-files; Defaults to False
- Prefix: Adds string as prefix to filename; Defaults to none
- Suffix: Adds string as suffix to filename; Defaults to none
- ThemeSound: Choosing theme based on [chime](https://github.com/MaxHalford/chime), or 'None' to disable it; Defaults to 'big-sur'

### Hotkeys

- Exit: Press this button to close the app which also cleans itself from drivers and temporary files; Defaults to F4
- DirectDownload: Press this button for a direct download; Defaults to F8
- IndirectDownload: Press this button for a indirect download; Defaults to F9
- NextPage: Press this button to navigate to the next page; Defaults to Right
- PreviousPage: Press this button to navigate to the previous page; Defaults to Left

### Paths
- OutputDirectory: Path to folder where downloads should end up at
- NextPageImg: Path for image of next button
- PreviousPageImg: Path for image of previous button

### XPath

- String1 = XPath to element that contains text, added first
- String2 = XPath to element that contains text, added secondly
- MoveIntoURL = XPath to a clickable element to be used for a *Indirect download*
- FileDownload = XPath to a clickable element for file download
- Gatekeeper = XPath to a clickable element that is gatekeeping content loading (e.g. age restrictions)

## Code of Conduct

Use at you own risk and discretion. Even though this is a semi-automatic web scraping in which only a single file can be downloaded at a time and cannot be automated to a larger extent. Do take in mind the **Terms of Service** of the website you are using this app for. **Be a good web scraper!**