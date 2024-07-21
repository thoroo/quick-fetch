# QuickFetch
QuickFetch is a Python script designed to automate the process of downloading a file or image from an active web browser tab when a keyboard button is pressed. It uses `pyautogui` to interact with the user's system and `selenium` to control a headless Chrome driver. QuickFetch is primarily designed for personal use but should be flexible enough to be applicable to other situations.

The script is a semi-automated tool that requires user input and is intended to reduce the time spent on downloading individual items in a page that use a grid or lazy loading. It uses `PyScreeze` to locate and interact with images on the screen for quick navigation.

### Key features

- **Multi-page support**: Quickly navigate between pages using keyboard shortcuts.
- **Flexible download options**: Choose from direct or indirect downloads for images and files.
- **Customizable download paths**: Specify a user-defined directory for all downloads.
- **Metadata-based file naming**: Customize file names using metadata from web elements.
- **Zip file extraction**: Automatically unzip downloaded files.
- **Interactive console**: Enjoy a clean and colorful console experience with rich logging.
- **Sound notifications**: Receive audio cues for successful or failed downloads.

### Current issues

- Checking for downloaded files has a timeout for 120 seconds. If download speed is low or if the file is large enough, it will cut off the download and close the application

## Installation

```bash
git clone https://github.com/phiido/quick-fetch
cd quick-fetch
```

- Note that QuickFetch **requires** '>= Python 3.8.0'
- Currently **only** runs using Chrome driver

## Usage
You just run call using a CLI or run the attached bat-file.

```bash
python3 -m quick_fetch
```

Currently, fetching images directly is the fastest way to download as it doesn't need to use the headless Chrome driver. For the others, there is a slight delay as the page needs to be loaded in the driver, downloaded to a temporary folder and then moved to the output folder.

If you want to use page navigator buttons, create a copy of the button image(s) (by taking a screenshot and then cropping the image) that are present on screen in the Chrome window, they can be setup anywhere as config reads which paths where they are located. However, a folder named './resources/' is created for the purpose of storing them.

Finding XPaths for an element can be done by going into DevTools (pressing F12 for Chrome), right clicking on the target element and copy the XPath string. A good tutorial can be found at [W3schools](https://www.w3schools.com/xml/xpath_intro.asp) for more advanced search methods. Double check that the XPath is correct by doing a search (CTRL + F) inside the elements tab of DevTools. You should only get a single hit, if it is 0 or >1, rewrite it.

**Note:** There is some validation of button clicks and copied URLs when using `Mouse mode`, however, Chrome has implemented quick access to *Reading Mode* that will be opened instead when pressing the hotkey for `Direct download` when hovering over a non-link element. A workaround is to disable *Reading Mode* from Chrome flags (<chrome://flags/>).

## Config settings

### General Settings
- **Custom Sound Theme**: Choosing theme based on [chime](https://github.com/MaxHalford/chime), or 'None' to disable it; Defaults to 'big-sur'
- **Log Level**: Can be changed for more output. If set to debug, the Chrome window will also show.

### Hotkeys
You can configure custom hotkeys for the following actions:
- **Exit**: Closes the application and cleans up anything related to the Chrome driver. Defaults to F4.
- **Direct Download**: Key to initiate a direct download (i.e., downloading from the current page).
- **Indirect Download**: Key to initiate an indirect download (i.e., downloading from another page found on the current page).
- **Next Page**: Key to move to the next page.
- **Previous Page**: Key to move to the previous page.

### Instructions

The keys of the instructions are as follows:
- `output - Path`: Sets the output directory for the file
- `page_next - Path`: Sets the button image for the button to take one to the next page
- `page_prev - Path`: Sets the button image for the button to take one to the previous page
- `click - XPath`: Clicks on a given XPath element
- `gatekeeper - XPath`: Works the same as click but only expects it once, for example a window pop up asking about cookies may block the screen.
- `url_from_mouse - image or link`: Grabs the URL from the mouse pointer, either image or link URL
- `url_from_window - None`: 
- `move_into_url - None`: Navigates to the given URL in Chrome
- `download - XPath or subset`:
    - `method - image or file`: Sets the type of download (image, file)
    - `xpath - XPath`: Sets the XPath element to download
    - `attr - string`: Sets the attribute to download (e.g. `src` for an image)
    - `rename_file`:
        - `format`: Set the format of the file
        - `add_prefix`: Adds a prefix to the file name
        - `add_suffix`: Adds a suffix to the file name

A example instruction can be found below. For example, the hotkey for indirect download (F9) will run the actions defined in the 'indirect' key. It does so by first grabbing the link URL from the mouse pointer, then opens a headless window to open that URL, clicks on a XPath element, downloads a image file by getting the URL attribute (in this case 'src') to download from.

Note that non-unique keys gets pruned in json5 and if you are for example doing multiple `click`'s, just add a number after it; e.g `click`, `click2`, etc.. As long the key starts with correct string.

**Example instruction:**
```json5
{
    example_image: {
        output: 'C:/downloads',
        direct: {
            url_from_mouse: 'image',
            download: 'image'
        },

        indirect: {
            url_from_mouse: 'link',
            move_to_url: '',
            click: '//*[@id="main"]/main/div/button',
            download: {
                method: 'image',
                xpath: '//*[@id="main"]/main/div/img',
                attr: 'src'
            }
        }
    },

    example_file: {
        output: 'C:/downloads',
        direct: {
            url_from_window: '',
            move_to_url: '',
            gatekeeper: '//button[contains(@onClick, "accept-all")]',
            download: '//p[contains(@class, "download")]/a[1]'
        },

        indirect: {
            url_from_window: '',
            move_to_url: '',
            gatekeeper: '//button[contains(@onClick, "accept-all")]',
            download: '//p[contains(@class, "download")]/a[1]'
        }
    }
}
```

## Code of Conduct
Use at you own risk and discretion. Even though this is a semi-automatic web scraping in which only a single file can be downloaded at a time and cannot be automated to a larger extent. Do take in mind the **Terms of Service** of the website you are using this app for. **Be a good web scraper!**