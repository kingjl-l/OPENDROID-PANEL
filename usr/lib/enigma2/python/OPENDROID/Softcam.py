from Components.Console import Console
from os import mkdir, path, remove
from glob import glob
from Components.config import config, ConfigSubsection, ConfigInteger, ConfigText, getConfigListEntry, ConfigSelection,  ConfigIP, ConfigYesNo, ConfigSequence, ConfigNumber, NoSave, ConfigEnableDisable, configfile
import os
config.Softcam.camdir = ConfigText(default = "/usr/emu", fixed_size=False)
config.Softcam.camconfig = ConfigText(default = "/usr/keys", fixed_size=False)
def getcamcmd(cam):
	camname = cam.lower()
	xcamname = cam
	if getcamscript(camname):
		return config.Softcam.camdir.value + "/" + cam + " start"
	elif ".x" in camname:
	        if "mgcamd" in camname: 
	        	return config.Softcam.camdir.value + "/" + cam
	        else:	
			emus=[]
			i = 0
			for fAdd in glob ('/etc/*.emu'):
				searchfile = open(fAdd, "r")
				emustart=[]
				cam_name = xcamname.strip(".x")
				for line in searchfile:
					if "binname" in line:
						emus.append(line[10:])
						if cam_name in emus[i]:
						        searchemu = open(fAdd, "r")
					                for line in searchemu:
								if "startcam" in line:
                                                			emustart.append(line[11:])
                                                			emustart = emustart[0].strip()
                                                			cam_count_test = emustart.count(" ")
                                                 			start_emu = emustart.split(" ", 1 )
                                                 			if (cam_count_test == 0):
                                                 				return config.Softcam.camdir.value + "/" + cam
                                                 			else: 
                                                    				return config.Softcam.camdir.value + "/" + cam + " " + start_emu[1]
                        	i = i + 1                        	
				searchfile.close()
	
	else:
		if "oscam" in camname:
			return config.Softcam.camdir.value + "/" + cam + " -bc " + \
				config.Softcam.camconfig.value + "/"
		if "doscam" in camname:
			return config.Softcam.camdir.value + "/" + cam + " -bc " + \
				config.Softcam.camconfig.value + "/"				
		elif "wicard" in camname:
			return "ulimit -s 512; " + config.Softcam.camdir.value + \
			"/" + cam + " -d -c " + config.Softcam.camconfig.value + \
			"/wicardd.conf"
		elif "camd3" in camname:
			return config.Softcam.camdir.value + "/" + cam + " " + \
				config.Softcam.camconfig.value + "/camd3.config"
		elif "mbox" in camname:
			return config.Softcam.camdir.value + "/" + cam + " " + \
				config.Softcam.camconfig.value + "/mbox.cfg"
		elif "cccam" in camname:
			return config.Softcam.camdir.value + "/" + cam + " -C " + \
				config.Softcam.camconfig.value + "/CCcam.cfg"
                elif "mgcamd" in camname:
	                os.system("rm /dev/dvb/adapter0/ca1")
	                os.system("ln -sf 'ca0' '/dev/dvb/adapter0/ca1'")                 
			return config.Softcam.camdir.value + "/" + cam + " -bc " + \
				config.Softcam.camconfig.value + "/"                				
		elif "mpcs" in camname:
			return config.Softcam.camdir.value + "/" + cam + " -c " + \
				config.Softcam.camconfig.value
		elif "newcs" in camname:
			return config.Softcam.camdir.value + "/" + cam + " -C " + \
				config.Softcam.camconfig.value + "/newcs.conf"
		elif "vizcam" in camname:
			return config.Softcam.camdir.value + "/" + cam + " -b -c " + \
				config.Softcam.camconfig.value + "/"
		elif "rucam" in camname:
			return config.Softcam.camdir.value + "/" + cam + " -b"
 		elif "scam" in camname and not "oscam" in camname:
			return config.Softcam.camdir.value + "/" + cam + " -s " + \
				config.Softcam.camconfig.value + "/"			
		else:
			return config.Softcam.camdir.value + "/" + cam

def getcamscript(cam):
	cam = cam.lower()
	if cam.endswith('.sh') or cam.startswith('softcam') or \
		cam.startswith('cardserver'):
		return True
	else:
		return False

def stopcam(cam):
	if getcamscript(cam):
		cmd = config.Softcam.camdir.value + "/" + cam + " stop"
	else:
		cmd = "killall -15 " + cam
	Console().ePopen(cmd)
	print "[SoftCam Manager] stopping", cam
	try:
		remove("/tmp/ecm.info")
	except:
		pass

def __createdir(list):
	dir = ""
	for line in list[1:].split("/"):
		dir += "/" + line
		if not path.exists(dir):
			try:
				mkdir(dir)
			except:
				print "[SoftCam Manager] Failed to mkdir", dir

def checkconfigdir():
	if not path.exists(config.Softcam.camconfig.value):
		__createdir("/usr/keys")
		config.Softcam.camconfig.value = "/usr/keys"
		config.Softcam.camconfig.save()
	if not path.exists(config.Softcam.camdir.value):
		if path.exists("/usr/emu"):
			config.Softcam.camdir.value = "/usr/emu"
		else:
			__createdir("/usr/emu")
			config.Softcam.camdir.value = "/usr/emu"
		config.Softcam.camdir.save()
