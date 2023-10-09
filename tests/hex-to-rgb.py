import re

def hex_to_rgb(hex_color):
  if hex_color is not None and len(hex_color) == 6:
    return str(tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)))

PALETTES = {
'Apprentice':
"""
name: 'Apprentice'

color_01: '#1C1C1C'    # Black (Host)
color_02: '#AF5F5F'    # Red (Syntax string)
color_03: '#5F875F'    # Green (Command)
color_04: '#87875F'    # Yellow (Command second)
color_05: '#5F87AF'    # Blue (Path)
color_06: '#5F5F87'    # Magenta (Syntax var)
color_07: '#5F8787'    # Cyan (Prompt)
color_08: '#6C6C6C'    # White

color_09: '#444444'    # Bright Black
color_10: '#FF8700'    # Bright Red (Command error)
color_11: '#87AF87'    # Bright Green (Exec)
color_12: '#FFFFAF'    # Bright Yellow
color_13: '#8FAFD7'    # Bright Blue (Folder)
color_14: '#8787AF'    # Bright Magenta
color_15: '#5FAFAF'    # Bright Cyan
color_16: '#FFFFFF'    # Bright White

background: '#262626'  # Background
foreground: '#BCBCBC'  # Foreground (Text)
""",

'Borland':
"""
name: 'Borland'

color_01: '#4F4F4F'    # Black (Host)
color_02: '#FF6C60'    # Red (Syntax string)
color_03: '#A8FF60'    # Green (Command)
color_04: '#FFFFB6'    # Yellow (Command second)
color_05: '#96CBFE'    # Blue (Path)
color_06: '#FF73FD'    # Magenta (Syntax var)
color_07: '#C6C5FE'    # Cyan (Prompt)
color_08: '#EEEEEE'    # White

color_09: '#7C7C7C'    # Bright Black
color_10: '#FFB6B0'    # Bright Red (Command error)
color_11: '#CEFFAC'    # Bright Green (Exec)
color_12: '#FFFFCC'    # Bright Yellow
color_13: '#B5DCFF'    # Bright Blue (Folder)
color_14: '#FF9CFE'    # Bright Magenta
color_15: '#DFDFFE'    # Bright Cyan
color_16: '#FFFFFF'    # Bright White

background: '#0000A4'  # Background
foreground: '#FFFF4E'  # Foreground (Text)
""",

'C64':
"""
name: 'C64'

color_01: '#090300'    # Black (Host)
color_02: '#883932'    # Red (Syntax string)
color_03: '#55A049'    # Green (Command)
color_04: '#BFCE72'    # Yellow (Command second)
color_05: '#40318D'    # Blue (Path)
color_06: '#8B3F96'    # Magenta (Syntax var)
color_07: '#67B6BD'    # Cyan (Prompt)
color_08: '#FFFFFF'    # White

color_09: '#000000'    # Bright Black
color_10: '#883932'    # Bright Red (Command error)
color_11: '#55A049'    # Bright Green (Exec)
color_12: '#BFCE72'    # Bright Yellow
color_13: '#40318D'    # Bright Blue (Folder)
color_14: '#8B3F96'    # Bright Magenta
color_15: '#67B6BD'    # Bright Cyan
color_16: '#F7F7F7'    # Bright White

background: '#40318D'  # Background
foreground: '#7869C4'  # Foreground (Text)
""",

'Dracula':
"""
name: 'Dracula'

color_01: '#44475A'    # Black (Host)
color_02: '#FF5555'    # Red (Syntax string)
color_03: '#50FA7B'    # Green (Command)
color_04: '#FFB86C'    # Yellow (Command second)
color_05: '#8BE9FD'    # Blue (Path)
color_06: '#BD93F9'    # Magenta (Syntax var)
color_07: '#FF79C6'    # Cyan (Prompt)
color_08: '#f8f8f2'    # White

color_09: '#000000'    # Bright Black
color_10: '#FF5555'    # Bright Red (Command error)
color_11: '#50FA7B'    # Bright Green (Exec)
color_12: '#FFB86C'    # Bright Yellow
color_13: '#8BE9FD'    # Bright Blue (Folder)
color_14: '#BD93F9'    # Bright Magenta
color_15: '#FF79C6'    # Bright Cyan
color_16: '#FFFFFF'    # Bright White

background: '#282A36'  # Background
foreground: '#f8f8f2'  # Foreground (Text)
""",

'Elemental':
"""
name: 'Elemental'

color_01: '#3C3C30'    # Black (Host)
color_02: '#98290F'    # Red (Syntax string)
color_03: '#479A43'    # Green (Command)
color_04: '#7F7111'    # Yellow (Command second)
color_05: '#497F7D'    # Blue (Path)
color_06: '#7F4E2F'    # Magenta (Syntax var)
color_07: '#387F58'    # Cyan (Prompt)
color_08: '#807974'    # White

color_09: '#555445'    # Bright Black
color_10: '#E0502A'    # Bright Red (Command error)
color_11: '#61E070'    # Bright Green (Exec)
color_12: '#D69927'    # Bright Yellow
color_13: '#79D9D9'    # Bright Blue (Folder)
color_14: '#CD7C54'    # Bright Magenta
color_15: '#59D599'    # Bright Cyan
color_16: '#FFF1E9'    # Bright White

background: '#22211D'  # Background
foreground: '#807A74'  # Foreground (Text)
""",

'Fairy Floss':
"""
name: 'Fairy Floss'

color_01: '#42395D'    # Black (Host)
color_02: '#A8757B'    # Red (Syntax string)
color_03: '#FF857F'    # Green (Command)
color_04: '#E6C000'    # Yellow (Command second)
color_05: '#AE81FF'    # Blue (Path)
color_06: '#716799'    # Magenta (Syntax var)
color_07: '#C2FFDF'    # Cyan (Prompt)
color_08: '#F8F8F2'    # White

color_09: '#75507B'    # Bright Black
color_10: '#FFB8D1'    # Bright Red (Command error)
color_11: '#F1568E'    # Bright Green (Exec)
color_12: '#D5A425'    # Bright Yellow
color_13: '#C5A3FF'    # Bright Blue (Folder)
color_14: '#8077A8'    # Bright Magenta
color_15: '#C2FFFF'    # Bright Cyan
color_16: '#F8F8F0'    # Bright White

background: '#5A5475'  # Background
foreground: '#C2FFDF'  # Foreground (Text)
""",

'Gruvbox':
"""
name: 'Gruvbox'

color_01: '#FBF1C7'    # Black (Host)
color_02: '#CC241D'    # Red (Syntax string)
color_03: '#98971A'    # Green (Command)
color_04: '#D79921'    # Yellow (Command second)
color_05: '#458588'    # Blue (Path)
color_06: '#B16286'    # Magenta (Syntax var)
color_07: '#689D6A'    # Cyan (Prompt)
color_08: '#7C6F64'    # White

color_09: '#928374'    # Bright Black
color_10: '#9D0006'    # Bright Red (Command error)
color_11: '#79740E'    # Bright Green (Exec)
color_12: '#B57614'    # Bright Yellow
color_13: '#076678'    # Bright Blue (Folder)
color_14: '#8F3F71'    # Bright Magenta
color_15: '#427B58'    # Bright Cyan
color_16: '#3C3836'    # Bright White

background: '#FBF1C7'  # Background
foreground: '#3C3836'  # Foreground (Text)
""",

'Gruvbox Dark':
"""
name: 'Gruvbox Dark'

color_01: '#282828'    # Black (Host)
color_02: '#CC241D'    # Red (Syntax string)
color_03: '#98971A'    # Green (Command)
color_04: '#D79921'    # Yellow (Command second)
color_05: '#458588'    # Blue (Path)
color_06: '#B16286'    # Magenta (Syntax var)
color_07: '#689D6A'    # Cyan (Prompt)
color_08: '#A89984'    # White

color_09: '#928374'    # Bright Black
color_10: '#FB4934'    # Bright Red (Command error)
color_11: '#B8BB26'    # Bright Green (Exec)
color_12: '#FABD2F'    # Bright Yellow
color_13: '#83A598'    # Bright Blue (Folder)
color_14: '#D3869B'    # Bright Magenta
color_15: '#8EC07C'    # Bright Cyan
color_16: '#EBDBB2'    # Bright White

background: '#282828'  # Background
foreground: '#EBDBB2'  # Foreground (Text)
""",

'Ibm3270':
"""
name: 'Ibm3270'

color_01: '#222222'    # Black (Host)
color_02: '#F01818'    # Red (Syntax string)
color_03: '#24D830'    # Green (Command)
color_04: '#F0D824'    # Yellow (Command second)
color_05: '#7890F0'    # Blue (Path)
color_06: '#F078D8'    # Magenta (Syntax var)
color_07: '#54E4E4'    # Cyan (Prompt)
color_08: '#A5A5A5'    # White

color_09: '#888888'    # Bright Black
color_10: '#EF8383'    # Bright Red (Command error)
color_11: '#7ED684'    # Bright Green (Exec)
color_12: '#EFE28B'    # Bright Yellow
color_13: '#B3BFEF'    # Bright Blue (Folder)
color_14: '#EFB3E3'    # Bright Magenta
color_15: '#9CE2E2'    # Bright Cyan
color_16: '#FFFFFF'    # Bright White

background: '#000000'  # Background
foreground: '#FDFDFD'  # Foreground (Text)
""",

'Kokuban':
"""
name: 'Kokuban'

color_01: '#2E8744'    # Black (Host)
color_02: '#D84E4C'    # Red (Syntax string)
color_03: '#95DA5A'    # Green (Command)
color_04: '#D6E264'    # Yellow (Command second)
color_05: '#4B9ED7'    # Blue (Path)
color_06: '#945FC5'    # Magenta (Syntax var)
color_07: '#D89B25'    # Cyan (Prompt)
color_08: '#D8E2D7'    # White

color_09: '#34934F'    # Bright Black
color_10: '#FF4F59'    # Bright Red (Command error)
color_11: '#AFF56A'    # Bright Green (Exec)
color_12: '#FCFF75'    # Bright Yellow
color_13: '#57AEFF'    # Bright Blue (Folder)
color_14: '#AE63E9'    # Bright Magenta
color_15: '#FFAA2B'    # Bright Cyan
color_16: '#FFFEFE'    # Bright White

background: '#0D4A08'  # Background
foreground: '#D8E2D7'  # Foreground (Text)
""",

'Lunaria Dark':
"""
name: 'Lunaria Dark'

color_01: '#36464E'    # Black (Host)
color_02: '#846560'    # Red (Syntax string)
color_03: '#809984'    # Green (Command)
color_04: '#A79A79'    # Yellow (Command second)
color_05: '#555673'    # Blue (Path)
color_06: '#866C83'    # Magenta (Syntax var)
color_07: '#7E98B4'    # Cyan (Prompt)
color_08: '#CACED8'    # White

color_09: '#404F56'    # Bright Black
color_10: '#BB928B'    # Bright Red (Command error)
color_11: '#BFDCC2'    # Bright Green (Exec)
color_12: '#F1DFB6'    # Bright Yellow
color_13: '#777798'    # Bright Blue (Folder)
color_14: '#BF9DB9'    # Bright Magenta
color_15: '#BDDCFF'    # Bright Cyan
color_16: '#DFE2ED'    # Bright White

background: '#36464E'  # Background
foreground: '#CACED8'  # Foreground (Text)
""",

'Lunaria Light':
"""
name: 'Lunaria Light'

color_01: '#3E3C3D'    # Black (Host)
color_02: '#783C1F'    # Red (Syntax string)
color_03: '#497D46'    # Green (Command)
color_04: '#8F750B'    # Yellow (Command second)
color_05: '#3F3566'    # Blue (Path)
color_06: '#793F62'    # Magenta (Syntax var)
color_07: '#3778A9'    # Cyan (Prompt)
color_08: '#D5CFCC'    # White

color_09: '#484646'    # Bright Black
color_10: '#B06240'    # Bright Red (Command error)
color_11: '#7BC175'    # Bright Green (Exec)
color_12: '#DCB735'    # Bright Yellow
color_13: '#5C4F89'    # Bright Blue (Folder)
color_14: '#B56895'    # Bright Magenta
color_15: '#64BAFF'    # Bright Cyan
color_16: '#EBE4E1'    # Bright White

background: '#EBE4E1'  # Background
foreground: '#484646'  # Foreground (Text)
""",

'Monokai Pro':
"""
name: 'Monokai Pro'

color_01: '#363537'    # Black (Host)
color_02: '#FF6188'    # Red (Syntax string)
color_03: '#A9DC76'    # Green (Command)
color_04: '#FFD866'    # Yellow (Command second)
color_05: '#FC9867'    # Blue (Path)
color_06: '#AB9DF2'    # Magenta (Syntax var)
color_07: '#78DCE8'    # Cyan (Prompt)
color_08: '#FDF9F3'    # White

color_09: '#908E8F'    # Bright Black
color_10: '#FF6188'    # Bright Red (Command error)
color_11: '#A9DC76'    # Bright Green (Exec)
color_12: '#FFD866'    # Bright Yellow
color_13: '#FC9867'    # Bright Blue (Folder)
color_14: '#AB9DF2'    # Bright Magenta
color_15: '#78DCE8'    # Bright Cyan
color_16: '#FDF9F3'    # Bright White

background: '#363537'  # Background
foreground: '#FDF9F3'  # Foreground (Text)
""",

'Papercolor Light':
"""
name: 'Papercolor Light'

color_01: '#EEEEEE'    # Black (Host)
color_02: '#AF0000'    # Red (Syntax string)
color_03: '#008700'    # Green (Command)
color_04: '#5F8700'    # Yellow (Command second)
color_05: '#0087AF'    # Blue (Path)
color_06: '#878787'    # Magenta (Syntax var)
color_07: '#005F87'    # Cyan (Prompt)
color_08: '#444444'    # White

color_09: '#BCBCBC'    # Bright Black
color_10: '#D70000'    # Bright Red (Command error)
color_11: '#D70087'    # Bright Green (Exec)
color_12: '#8700AF'    # Bright Yellow
color_13: '#D75F00'    # Bright Blue (Folder)
color_14: '#D75F00'    # Bright Magenta
color_15: '#005FAF'    # Bright Cyan
color_16: '#005F87'    # Bright White

background: '#EEEEEE'  # Background
foreground: '#444444'  # Foreground (Text)
""",

'Powershell':
"""
name: 'Powershell'

color_01: '#000000'    # Black (Host)
color_02: '#7E0008'    # Red (Syntax string)
color_03: '#098003'    # Green (Command)
color_04: '#C4A000'    # Yellow (Command second)
color_05: '#010083'    # Blue (Path)
color_06: '#D33682'    # Magenta (Syntax var)
color_07: '#0E807F'    # Cyan (Prompt)
color_08: '#7F7C7F'    # White

color_09: '#808080'    # Bright Black
color_10: '#EF2929'    # Bright Red (Command error)
color_11: '#1CFE3C'    # Bright Green (Exec)
color_12: '#FEFE45'    # Bright Yellow
color_13: '#268AD2'    # Bright Blue (Folder)
color_14: '#FE13FA'    # Bright Magenta
color_15: '#29FFFE'    # Bright Cyan
color_16: '#C2C1C3'    # Bright White

background: '#052454'  # Background
foreground: '#F6F6F7'  # Foreground (Text)
""",

'Seafoam Pastel':
"""
name: 'Seafoam Pastel'

color_01: '#757575'    # Black (Host)
color_02: '#825D4D'    # Red (Syntax string)
color_03: '#728C62'    # Green (Command)
color_04: '#ADA16D'    # Yellow (Command second)
color_05: '#4D7B82'    # Blue (Path)
color_06: '#8A7267'    # Magenta (Syntax var)
color_07: '#729494'    # Cyan (Prompt)
color_08: '#E0E0E0'    # White

color_09: '#8A8A8A'    # Bright Black
color_10: '#CF937A'    # Bright Red (Command error)
color_11: '#98D9AA'    # Bright Green (Exec)
color_12: '#FAE79D'    # Bright Yellow
color_13: '#7AC3CF'    # Bright Blue (Folder)
color_14: '#D6B2A1'    # Bright Magenta
color_15: '#ADE0E0'    # Bright Cyan
color_16: '#E0E0E0'    # Bright White

background: '#243435'  # Background
foreground: '#D4E7D4'  # Foreground (Text)
""",

'Solarized Dark':
"""
name: 'Solarized Dark'

color_01: '#073642'    # Black (Host)
color_02: '#DC322F'    # Red (Syntax string)
color_03: '#859900'    # Green (Command)
color_04: '#CF9A6B'    # Yellow (Command second)
color_05: '#268BD2'    # Blue (Path)
color_06: '#D33682'    # Magenta (Syntax var)
color_07: '#2AA198'    # Cyan (Prompt)
color_08: '#EEE8D5'    # White

color_09: '#657B83'    # Bright Black
color_10: '#D87979'    # Bright Red (Command error)
color_11: '#88CF76'    # Bright Green (Exec)
color_12: '#657B83'    # Bright Yellow
color_13: '#2699FF'    # Bright Blue (Folder)
color_14: '#D33682'    # Bright Magenta
color_15: '#43B8C3'    # Bright Cyan
color_16: '#FDF6E3'    # Bright White

background: '#002B36'  # Background
foreground: '#839496'  # Foreground (Text)
""",

'Solarized Light':
"""
name: 'Solarized Light'

color_01: '#073642'    # Black (Host)
color_02: '#DC322F'    # Red (Syntax string)
color_03: '#859900'    # Green (Command)
color_04: '#B58900'    # Yellow (Command second)
color_05: '#268BD2'    # Blue (Path)
color_06: '#D33682'    # Magenta (Syntax var)
color_07: '#2AA198'    # Cyan (Prompt)
color_08: '#EEE8D5'    # White

color_09: '#002B36'    # Bright Black
color_10: '#CB4B16'    # Bright Red (Command error)
color_11: '#586E75'    # Bright Green (Exec)
color_12: '#657B83'    # Bright Yellow
color_13: '#839496'    # Bright Blue (Folder)
color_14: '#6C71C4'    # Bright Magenta
color_15: '#93A1A1'    # Bright Cyan
color_16: '#FDF6E3'    # Bright White

background: '#FDF6E3'  # Background
foreground: '#657B83'  # Foreground (Text)
""",

'Spacegray':
"""
name: 'Spacegray'

color_01: '#000000'    # Black (Host)
color_02: '#B04B57'    # Red (Syntax string)
color_03: '#87B379'    # Green (Command)
color_04: '#E5C179'    # Yellow (Command second)
color_05: '#7D8FA4'    # Blue (Path)
color_06: '#A47996'    # Magenta (Syntax var)
color_07: '#85A7A5'    # Cyan (Prompt)
color_08: '#B3B8C3'    # White

color_09: '#000000'    # Bright Black
color_10: '#B04B57'    # Bright Red (Command error)
color_11: '#87B379'    # Bright Green (Exec)
color_12: '#E5C179'    # Bright Yellow
color_13: '#7D8FA4'    # Bright Blue (Folder)
color_14: '#A47996'    # Bright Magenta
color_15: '#85A7A5'    # Bright Cyan
color_16: '#FFFFFF'    # Bright White

background: '#20242D'  # Background
foreground: '#B3B8C3'  # Foreground (Text)
""",

'Zenburn':
"""
name: 'Zenburn'

color_01: '#4D4D4D'    # Black (Host)
color_02: '#705050'    # Red (Syntax string)
color_03: '#60B48A'    # Green (Command)
color_04: '#F0DFAF'    # Yellow (Command second)
color_05: '#506070'    # Blue (Path)
color_06: '#DC8CC3'    # Magenta (Syntax var)
color_07: '#8CD0D3'    # Cyan (Prompt)
color_08: '#DCDCCC'    # White

color_09: '#709080'    # Bright Black
color_10: '#DCA3A3'    # Bright Red (Command error)
color_11: '#C3BF9F'    # Bright Green (Exec)
color_12: '#E0CF9F'    # Bright Yellow
color_13: '#94BFF3'    # Bright Blue (Folder)
color_14: '#EC93D3'    # Bright Magenta
color_15: '#93E0E3'    # Bright Cyan
color_16: '#FFFFFF'    # Bright White

background: '#3F3F3F'  # Background
foreground: '#DCDCCC'  # Foreground (Text)
""",
}

PALETTES = {
'Kanagawa':
"""
name: 'Kanagawa'

color_01: '#090618'    # Black (Host)
color_02: '#C34043'    # Red (Syntax string)
color_03: '#76946A'    # Green (Command)
color_04: '#C0A36E'    # Yellow (Command second)
color_05: '#7E9CD8'    # Blue (Path)
color_06: '#957FB8'    # Magenta (Syntax var)
color_07: '#6A9589'    # Cyan (Prompt)
color_08: '#DCD7BA'    # White

color_09: '#727169'    # Bright Black
color_10: '#E82424'    # Bright Red (Command error)
color_11: '#98BB6C'    # Bright Green (Exec)
color_12: '#E6C384'    # Bright Yellow
color_13: '#7FB4CA'    # Bright Blue (Folder)
color_14: '#938AA9'    # Bright Magenta
color_15: '#7AA89F'    # Bright Cyan
color_16: '#C8C093'    # Bright White

background: '#1F1F28'  # Background
foreground: '#DCD7BA'  # Foreground (Text)
""",

'Maia':
"""
name: 'Maia'

color_01: '#232423'    # Black (Host)
color_02: '#BA2922'    # Red (Syntax string)
color_03: '#7E807E'    # Green (Command)
color_04: '#4C4F4D'    # Yellow (Command second)
color_05: '#16A085'    # Blue (Path)
color_06: '#43746A'    # Magenta (Syntax var)
color_07: '#00CCCC'    # Cyan (Prompt)
color_08: '#E0E0E0'    # White

color_09: '#282928'    # Bright Black
color_10: '#CC372C'    # Bright Red (Command error)
color_11: '#8D8F8D'    # Bright Green (Exec)
color_12: '#4E524F'    # Bright Yellow
color_13: '#13BF9D'    # Bright Blue (Folder)
color_14: '#487D72'    # Bright Magenta
color_15: '#00D1D1'    # Bright Cyan
color_16: '#E8E8E8'    # Bright White

background: '#31363B'  # Background
foreground: '#BDC3C7'  # Foreground (Text)
""",

'Man Page':
"""
name: 'Man Page'

color_01: '#000000'    # Black (Host)
color_02: '#CC0000'    # Red (Syntax string)
color_03: '#00A600'    # Green (Command)
color_04: '#999900'    # Yellow (Command second)
color_05: '#0000B2'    # Blue (Path)
color_06: '#B200B2'    # Magenta (Syntax var)
color_07: '#00A6B2'    # Cyan (Prompt)
color_08: '#CCCCCC'    # White

color_09: '#666666'    # Bright Black
color_10: '#E50000'    # Bright Red (Command error)
color_11: '#00D900'    # Bright Green (Exec)
color_12: '#E5E500'    # Bright Yellow
color_13: '#0000FF'    # Bright Blue (Folder)
color_14: '#E500E5'    # Bright Magenta
color_15: '#00E5E5'    # Bright Cyan
color_16: '#E5E5E5'    # Bright White

background: '#FEF49C'  # Background
foreground: '#000000'  # Foreground (Text)
""",

'N0Tch2K':
"""
name: 'N0Tch2K'

color_01: '#383838'    # Black (Host)
color_02: '#A95551'    # Red (Syntax string)
color_03: '#666666'    # Green (Command)
color_04: '#A98051'    # Yellow (Command second)
color_05: '#657D3E'    # Blue (Path)
color_06: '#767676'    # Magenta (Syntax var)
color_07: '#C9C9C9'    # Cyan (Prompt)
color_08: '#D0B8A3'    # White

color_09: '#474747'    # Bright Black
color_10: '#A97775'    # Bright Red (Command error)
color_11: '#8C8C8C'    # Bright Green (Exec)
color_12: '#A99175'    # Bright Yellow
color_13: '#98BD5E'    # Bright Blue (Folder)
color_14: '#A3A3A3'    # Bright Magenta
color_15: '#DCDCDC'    # Bright Cyan
color_16: '#D8C8BB'    # Bright White

background: '#222222'  # Background
foreground: '#A0A0A0'  # Foreground (Text)
""",

'Pnevma':
"""
name: 'Pnevma'

color_01: '#2F2E2D'    # Black (Host)
color_02: '#A36666'    # Red (Syntax string)
color_03: '#90A57D'    # Green (Command)
color_04: '#D7AF87'    # Yellow (Command second)
color_05: '#7FA5BD'    # Blue (Path)
color_06: '#C79EC4'    # Magenta (Syntax var)
color_07: '#8ADBB4'    # Cyan (Prompt)
color_08: '#D0D0D0'    # White

color_09: '#4A4845'    # Bright Black
color_10: '#D78787'    # Bright Red (Command error)
color_11: '#AFBEA2'    # Bright Green (Exec)
color_12: '#E4C9AF'    # Bright Yellow
color_13: '#A1BDCE'    # Bright Blue (Folder)
color_14: '#D7BEDA'    # Bright Magenta
color_15: '#B1E7DD'    # Bright Cyan
color_16: '#EFEFEF'    # Bright White

background: '#1C1C1C'  # Background
foreground: '#D0D0D0'  # Foreground (Text)
""",
}

COLOR_NAME = [
  "black",
  "red",
  "green",
  "yellow",
  "blue",
  "magenta",
  "cyan",
  "white",
  "bright_black",
  "bright_red",
  "bright_green",
  "bright_yellow",
  "bright_blue",
  "bright_magenta",
  "bright_cyan",
  "bright_white",
  "background",
  "foreground",
]

for name, colors in PALETTES.items():
  colors = re.findall("\'#(.{6})\'", colors)
  print('  "' + name + '": {')
  for num, line in enumerate(colors):
    line = '    "' + COLOR_NAME[num] + '": ' +hex_to_rgb(line) + ','
    print(line)
  print('  },')