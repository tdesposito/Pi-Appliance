# Appliance Feature Scripts

The folders herein enable individual features of the Pi.

Each folder contains an `enable_feature.sh` script which will be run during
initial setup if the feature is enabled in `application_config.json.` The script
contains header comments which help the `builder` and `installer` tools
determine how to handle the features.

## Feature Definition
The feature is defined by the `#%%` comment.
```console
#%% Name Of Feature
```

## Parameter Definition(s)
Parameters needed for the feature is defined on zero or more `#%@` comments.
```console
#%@ parameter_key Parameter Prompt
```

## Template File(s)
If you have parameters, they likely need to go somewhere. The `#%<` comment
defines a file **in the feature folder** which should be updated with the
parameters. These parameters will be added to the `application_config.json` file
written into the Pi's /boot partition by the `builder` tool.

```console
#%< template-file-name-here
```
The template itself won't be touched; the `installer` tool will convert the
template based on the parameters in `application_config.json` and the result
placed in a corresponding `/home/pi/.templatefiles` subdirectory.
