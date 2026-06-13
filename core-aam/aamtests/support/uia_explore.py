from unicodedata import name

import comtypes.client

import ctypes

from comtypes import COMError  # or whichever COM binding you use for raw native UIA

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

    UIA_PATTERN_ID_MAP = {
        value: name[len("UIA_"):-len("PatternId")]
        for name, value in vars(UIA).items()
        if name.startswith("UIA_") and name.endswith("PatternId")
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

    print("\n--- UIA Pattern ID Map ---")
    for pattern_id, name in UIA_PATTERN_ID_MAP.items():
        print(f"{pattern_id:<8} | {name}")

    # print(f"\nExample: The property ID for 'ControllerFor' is {getpropertyIdfromname('ControllerFor')}");
    print(f"UIA.UIA_ControllerForPropertyId: {UIA.UIA_ControllerForPropertyId}")
    print(f"UIA.UIA_LocalizedControlTypePropertyId: {UIA.UIA_LocalizedControlTypePropertyId}")

    # 4. Grab the absolute Root Element (The Windows Desktop)s
    root = _automation.GetRootElement()
    
    print("\n--- Directly Queried from UIAutomationCore.dll ---")
    print(f"Root Element Name:      {root.CurrentName}")
    print(f"Root Class Name:        {root.CurrentClassName}")
    print(f"Root Native Window ID:  {root.CurrentNativeWindowHandle}")
    print(f"Root Process ID:        {root.CurrentProcessId}")

    # def getPatterns(element):
    #     supported_patterns = []
        
    #     for pattern_id, pattern_name in UIA_PATTERN_ID_MAP.items():
    #         try:
    #             # Native COM returns a valid pointer object if supported.
    #             # If NOT supported, the native layer throws an HRESULT/COMError.
    #             pattern_obj = element.GetCurrentPattern(pattern_id)
                
    #             if pattern_obj:
    #                 supported_patterns.append(pattern_name)
    #         except (COMError, Exception):
    #             # Native UIA explicitly fails with an error code if the control doesn't support the pattern.
    #             continue
    #     return supported_patterns

    # def getAllPatterns(element):
    #     supported_patterns = []
        
    #     for pattern_id, pattern_name in UIA_PATTERN_ID_MAP.items():
    #         try:
    #             pattern_obj = element.GetCurrentPattern(pattern_id)
                
    #             if pattern_condition_is_valid(pattern_obj):
    #                 supported_patterns.append(pattern_name)
                    
    #         except Exception:
    #             continue
                
    #     return supported_patterns

    # def pattern_condition_is_valid(pattern_obj):
    #     if pattern_obj is None:
    #         return False
            
    #     # ctypes.cast turns the COM object into an explicit raw integer address.
    #     # If the address is 0, it means the pointer is 0x0 (Null).
    #     address = ctypes.cast(pattern_obj, ctypes.c_void_p(0x1234)).value
        
    #     # Explicitly check if the address exists and is not zero
    #     if address is not None and address != 0:
    #         return True
            
    #     return False
    
    # def pattern_condition_is_valid(pattern_obj):
    #     if pattern_obj is None:
    #         return False
            
    #     # ctypes.cast turns the COM object into an explicit raw integer address.
    #     # If the address is 0, it means the pointer is 0x0 (Null).
    #     address = ctypes.cast(pattern_obj, ctypes.c_void_p).value
        
    #     # Explicitly check if the address exists and is not zero
    #     if address is not None and address != 0:
    #         return True
            
    #     return False

    def getAllPatterns2(element):
        for pattern_id, pattern_name in UIA_PATTERN_ID_MAP.items():
            try:
                pattern_obj = element.GetCurrentPattern(pattern_id)

                if pattern_obj :
                    if pattern_name == "Toggle" :
                        togglePatern = pattern_obj.QueryInterface(comtypes.gen.UIAutomationClient.IUIAutomationTogglePattern)
                        print(f"ToggleState: {togglePatern.CurrentToggleState}")
                        #print(f"{element.GetCurrentPropertyValue(UIA.UIA_ToggleToggleStatePropertyId)}")
                    elif pattern_name == "SelectionItem" :
                        selectionPatern = pattern_obj.QueryInterface(comtypes.gen.UIAutomationClient.IUIAutomationSelectionItemPattern)
                        print(f"IsSelected: {selectionPatern.CurrentIsSelected}")
                        #print(f"{element.GetCurrentPropertyValue(UIA.UIA_SelectionItemIsSelectedPropertyId)}")
                    elif pattern_name == "Text" :
                        TextPatern = pattern_obj.QueryInterface(comtypes.gen.UIAutomationClient.IUIAutomationTextPattern)
                        text_range = TextPatern.DocumentRange
                        print(f"IsSuperscript: {text_range.GetAttributeValue(UIA.UIA_IsSuperscriptAttributeId)}")
                        print(f"IsSubscript: {text_range.GetAttributeValue(UIA.UIA_IsSubscriptAttributeId)}")
                print(f"{pattern_name}: type={type(pattern_obj)} | repr={repr(pattern_obj)}")
            except Exception as e:
                print(f"{pattern_name}: Threw error {e}")

    # 5. Recursively explore the tree of control elements under the root, printing their names and class names
    # def getfullTree (element, indent=0):
    #     print(f"{' ' * indent}- {element.CurrentName} {getAllPatterns2(element)}")
    #     children = element.FindAll(UIA.TreeScope_Children, _automation.CreatePropertyCondition(UIA.UIA_IsControlElementPropertyId, True))
    #     for i in range(children.Length):
    #         getfullTree(children.GetElement(i), indent + 2)
    # print("\n--- Full Tree of Control Elements under Root ---")
    # getfullTree(root)


    # Find the first child element of the root that is a control element and more than one patterns available, and print its name and supported patterns
    # condition = _automation.CreatePropertyCondition(UIA.UIA_IsControlElementPropertyId, True)
    # # Descendants ensures we peek inside windows to find rich controls
    # controls = root.FindAll(UIA.TreeScope_Descendants, condition)

    # print(f"Total elements scanned: {controls.Length}")

    # for i in range(controls.Length):
    #     element = controls.GetElement(i)
    #     patterns = getAllPatterns(element)
        
    #     if len(patterns) > 1:
    #         print(f"\n--- Found One! ---")
    #         print(f"Name: {element.CurrentName}")
    #         print(f"Class Name: {element.CurrentClassName}")
    #         print(f"Native Window ID: {element}")
    #         print(f"Supported Patterns: {patterns}")
    #         break

    # 1. Create a condition that filters for the Button Control Type
    # 50000 is the native UIA_ButtonControlTypeId
    button_condition = _automation.CreatePropertyCondition(
        UIA.UIA_ControlTypePropertyId, UIA.UIA_ButtonControlTypeId  # 30003 = UIA_ControlTypePropertyId
    )

    # 50002 is the toggle
    checkBox_condition = _automation.CreatePropertyCondition(
        UIA.UIA_ControlTypePropertyId, UIA.UIA_CheckBoxControlTypeId
    )

    text_condition = _automation.CreatePropertyCondition(
        UIA.UIA_ControlTypePropertyId, UIA.UIA_TextControlTypeId
    )

    listItem_Condition = _automation.CreatePropertyCondition(
        UIA.UIA_ControlTypePropertyId, UIA.UIA_ListItemControlTypeId
    )

    # 2. (Optional) If you want a SPECIFIC button, combine it with a Name condition
    name_conditiontoggle = _automation.CreatePropertyCondition(
        UIA.UIA_NamePropertyId, "Option 1 (Checkbox)"  # 30005 = UIA_NamePropertyId, "Google Search" is the button text
    )

    name_conditionsup = _automation.CreatePropertyCondition(
        UIA.UIA_NamePropertyId, "2"
    )

    name_conditionListItem = _automation.CreatePropertyCondition(
        UIA.UIA_NamePropertyId, "Apple"
    )

    # Combine them so it looks for a Button named "Google Search"
    target_condition_toggle = _automation.CreateAndCondition(checkBox_condition, name_conditiontoggle)

    target_condition_text = _automation.CreateAndCondition(text_condition, name_conditionsup)

    target_condition_listItem = _automation.CreateAndCondition(listItem_Condition, name_conditionListItem)

    toggle = root.FindFirst(UIA.TreeScope_Descendants, target_condition_toggle)

    text = root.FindFirst(UIA.TreeScope_Descendants, target_condition_text)

    listItem = root.FindFirst(UIA.TreeScope_Descendants, target_condition_listItem)

    if toggle:
        print(f"Successfully grabbed target element: '{toggle.CurrentName}'")
        
        # Run your pattern inspector on just this one element
        patterns_toggle = getAllPatterns2(toggle)
        print(f"Supported Patterns: {patterns_toggle}")
    else:
        print("Could not find a toggle matching that criteria.")


    if text:
        print(f"Successfully grabbed target element: '{text.CurrentName}'")
        
        # Run your pattern inspector on just this one element
        patterns_text = getAllPatterns2(text)
        print(f"Supported Patterns: {patterns_text}")

    else:
        print("Could not find a text matching that criteria.")

    if listItem:
        print(f"Successfully grabbed target element: '{text.CurrentName}'")
        
        # Run your pattern inspector on just this one element
        patterns_text = getAllPatterns2(listItem)
        print(f"Supported Patterns: {patterns_text}")

    else:
        print("Could not find a listItem matching that criteria.")

if __name__ == "__main__":
    explore_raw_dll()