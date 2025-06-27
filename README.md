# MJCF2USD

A powerful Omniverse extension for converting MuJoCo XML Configuration Format (MJCF) files to Universal Scene Description (USD) format.

**Lightwheel is hiring!** 

If you're interested in joining our team, please contact Frank Chen: **ming.chen@lightwheel.ai**


## Overview

MJCF2USD is a user-friendly tool that enables seamless conversion of MuJoCo simulation files to USD format, making it easy to integrate MuJoCo models into Omniverse workflows and other USD-compatible applications.

## Features

- **Batch Conversion**: Convert multiple MJCF files at once
- **Intuitive UI**: Simple and clean interface with step-by-step guidance
- **Flexible Output**: Choose custom output locations or use default paths
- **Progress Tracking**: Real-time conversion progress with time estimates
- **Error Handling**: Detailed success/failure reporting
- **XML Modification**: Optional temporary XML file saving for debugging

## Installation

### Prerequisites

- NVIDIA Isaac Sim

### Installation Steps

1. Clone this repository to your Omniverse extensions directory:
   ```bash
   git clone <repository-url> /path/to/isaacsim/extensions
   ```

2. Enable the extension through the Extensions Manager in Isaac Sim.

3. **Set the Import Path in Isaac Sim:**
   - Open Isaac Sim and go to `Window` > `Extensions`.
   - Click the `Settings` (gear) icon.
   - In the `Extension Search Paths` section, click the `+` button.
   - Copy and paste the parent path of the `mjcf2usd` folder (the path where you cloned this repository).

> 📄 **For detailed step-by-step instructions with screenshots, please refer to [Installation.pdf](Installation.pdf) included in this repository.**

## Usage

### Getting Started

1. **Launch the Extension**: 
   - Open IsaacSim
   - Go to `Window` > `Extensions`.
   - Enable "MJCF2USD" extension
   - The MJCF2USD window will appear

2. **Select MJCF Files**:
   - Click "Select File or Folder" in step 1
   - Choose either a single MJCF file or a folder containing multiple MJCF files
   - The extension will automatically scan and list all found MJCF files

3. **Choose Output Location** (Optional):
   - Click "Select Folder" in step 2
   - Choose where you want the USD files to be saved
   - If left empty, USD files will be saved in the same directory as the MJCF files

4. **Configure Options**:
   - Check "Save Temp MJCF XML" if you want to save modified XML files for debugging

5. **Start Conversion**:
   - Click "MJCFs to USDs" button
   - Monitor the progress in the status area
   - View conversion results and timing information

### Output

- **Success**: USD files will be created in the specified output location
- **File Naming**: Output files follow the pattern `{parent_folder}_{filename}.usd`
- **Reports**: Detailed conversion statistics including:
  - Total conversion time
  - Number of successful conversions
  - Number of failed conversions
  - List of successful and failed files

## Project Structure

```
MJCF2USD/
├── config/
│   └── extension.toml          # Extension configuration
├── data/
│   ├── logo.png               # Extension icon
│   └── preview.jpeg           # Extension preview image
├── lightwheel/
│   └── MJCF2USD/
│       └── connection/
│           ├── extension.py   # Main extension entry point
│           ├── window.py      # UI window implementation
│           ├── mjcf2usd_utils.py  # Core conversion utilities
│           ├── option_widget.py   # UI components
│           ├── ui_utils.py    # UI utility functions
│           └── style.py       # UI styling
├── LICENSE.txt                # License file
└── README.md                  # This file
```

## Development

### Dependencies

- `omni.kit.uiapp`: Omniverse UI framework
- `omni.ui`: Omniverse UI components
- `omni.usd`: USD manipulation utilities
- `omni.kit.commands`: Omniverse command system

### Building

The extension is built using Omniverse Kit's extension system. No additional build steps are required beyond the standard Python module structure.

## Version

Current version: 1.0.0

## Support

For issues and questions, please contact the development team or create an issue in the repository.
