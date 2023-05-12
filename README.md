# ElegooN3Thumbnail &middot; [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
Cura 5.x plugin for including thumbnail/preview images in gcode files for Elegoo Neptune 3 Pro, Plus and Max.

<img src="images/n3pro.jpg" width="250">

## Installation

- Download the latest relase [here](https://github.com/sigathi/ElegooN3Thumbnail/releases/latest/download/ElegooN3Thumbnail.curapackage).
- Drag the `.curapackage` file onto Cura and restart Cura.

## Usage
To enable the plugin, add `;includeThumbnail` to the Start G-code in your machine settings:
- Open printer selection menu and choose `Manage Printers`  
![Manage printers](images/cura_manage_printers.png "Manage printers")
- Choose your Elegoo Neptune 3 Pro/Plus/Max printer  and then `Machine Settings`  
![Machine Settings](images/cura_machine_settings.png "Machine Settings")
- At the top of `Start G-code` add `;includeThumbnail`.
![Start G-code](images/cura_start_g-code.png "Start G-code")

## Contribution

This repository is based on [Toylerrr / ElegooNeptuneSnapshot ](https://github.com/Toylerrr/ElegooNeptuneSnapshot) and [daniel-kukiela / LotmaxxSnapshot](https://github.com/daniel-kukiela/LotmaxxSnapshot).
The image encoding binaries are exported from Elegoo Cura.
