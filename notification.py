import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom
import pathlib
import os, re

currentdir = pathlib.Path(__file__).parent.absolute()

class NotificationSender:
    def __init__(self):
        self.app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe'
        # self.app = '{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}\\Microsoft\\Teams\\Current\\Teams.exe'
        # self.app = '{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Teams'
        self.nManager = notifications.ToastNotificationManager
        self.notifier = self.nManager.create_toast_notifier(self.app)
    
    def welcome(self):
        text = """
            <toast>
                <visual>
                <binding template='ToastGeneric'>
                    <text>Valedict</text>
                    <text>Now running in the background</text>
                    <image placement="appLogoOverride" src="file:///{}/valedictlogo.png"/>
                </binding>
                </visual>
                <actions>
                <action
                    content="Delete"
                    arguments="action=launchApplication"/>
                <action
                    content="Dismiss"
                    arguments="action=dismiss"/>
                </actions>        
            </toast>
            """.format(currentdir)

        xDoc = dom.XmlDocument()
        xDoc.load_xml(text)

        self.notifier.show(notifications.ToastNotification(xDoc))

    def send(self, name, time):
        text = """
            <toast>
                <visual>
                <binding template='ToastGeneric'>
                    <text>{0}</text>
                    <text>Starting at {1}</text>
                    <image placement="appLogoOverride" src="file:///{2}/valedictlogo.png"/>
                </binding>
                </visual>
                <actions>
                <action
                    content="Delete"
                    arguments="action=launchApplication"/>
                <action
                    content="Dismiss"
                    arguments="action=dismiss"/>
                </actions>        
            </toast>
            """.format(name, time, currentdir)

        xDoc = dom.XmlDocument()
        xDoc.load_xml(text)

        self.notifier.show(notifications.ToastNotification(xDoc))
    
    def goodbye(self):
        text = """
            <toast>
                <visual>
                <binding template='ToastGeneric'>
                    <text>Valedict</text>
                    <text>Stopping...</text>
                    <image placement="appLogoOverride" src="file:///{}/valedictlogo.png"/>
                </binding>
                </visual>
                <actions>
                <action
                    content="Delete"
                    arguments="action=launchApplication"/>
                <action
                    content="Dismiss"
                    arguments="action=dismiss"/>
                </actions>        
            </toast>
            """.format(currentdir)

        xDoc = dom.XmlDocument()
        xDoc.load_xml(text)

        self.notifier.show(notifications.ToastNotification(xDoc))