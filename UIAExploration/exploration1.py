from unicodedata import name

import comtypes.client

def explore_raw_dll():
    print("Loading UIAutomationCore.dll interfaces...")
    
    # 1. Load the DLL type library. This creates the underlying Python bindings.
    UIA = comtypes.client.GetModule("UIAutomationCore.dll")


    # 2. Explicitly import the generated COM clients from the local cache
    from comtypes.gen.UIAutomationClient import CUIAutomation, IUIAutomation
    
    # 3. Instantiate the master UI Automation manager object
    _automation = comtypes.client.CreateObject(
    UIA.CUIAutomation, interface=UIA.IUIAutomation
    )

    
    # Map UIA control type ids (e.g. 50000) to readable names (e.g. "Button") by


    for name, value in vars(UIA).items():
        print(f"{name:<8} : {value}")

    # Generate a mapping of control type id to human readable name, e.g. 50000 -> "Button", 50001 -> "Calendar", etc.
    UIA_CONTROL_TYPE_MAP = {
        value: name[len("UIA_"):-len("ControlTypeId")]
        for name, value in vars(UIA).items()
        if name.startswith("UIA_") and name.endswith("ControlTypeId")
    }

    # Generate a mapping of property id to human readable name, e.g. 30000 -> "AutomationId", 30001 -> "Name", etc.
    UIA_PROPERTY_ID_MAP = {
        value: name[len("UIA_"):-len("PropertyId")]
        for name, value in vars(UIA).items()
        if name.startswith("UIA_") and name.endswith("PropertyId")
    }

    # Generate a mapping of event id to human readable name, e.g. 20000 -> "AutomationFocusChangedEvent", 20001 -> "AutomationPropertyChangedEvent", etc.
    UIA_EVENT_ID_MAP = {
        value: name[len("UIA_"):-len("EventId")]
        for name, value in vars(UIA).items()
        if name.startswith("UIA_") and name.endswith("EventId")
    }


    print("\n--- UIA Control Type Map ---")
    for control_id, name in UIA_CONTROL_TYPE_MAP.items():
        # The :<8 aligns the ID to the left inside an 8-character wide block
        print(f"{control_id:<8} | {name}")

    print("\n--- UIA Property ID Map ---")
    for property_id, name in UIA_PROPERTY_ID_MAP.items():
        print(f"{property_id:<8} | {name}")
    
    print("\n--- UIA Event ID Map ---")
    for event_id, name in UIA_EVENT_ID_MAP.items():
        print(f"{event_id:<8} | {name}")
    
    # print(f"\nExample: The property ID for 'ControllerFor' is {getpropertyIdfromname('ControllerFor')}");
    print(f"UIA.UIA_ControllerForPropertyId: {UIA.UIA_ControllerForPropertyId}")
    print(f"UIA.UIA_LocalizedControlTypePropertyId: {UIA.UIA_LocalizedControlTypePropertyId}")

    # 4. Grab the absolute Root Element (The Windows Desktop)
    root = _automation.GetRootElement()
    
    print("\n--- Directly Queried from UIAutomationCore.dll ---")
    print(f"Root Element Name:      {root.CurrentName}")
    print(f"Root Class Name:        {root.CurrentClassName}")
    print(f"Root Native Window ID:  {root.CurrentNativeWindowHandle}")
    print(f"Root Process ID:        {root.CurrentProcessId}")

if __name__ == "__main__":
    explore_raw_dll()