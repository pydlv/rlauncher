import configparser;

#read config
config = configparser.ConfigParser();
config.read("config.ini");
sections = config.sections();

def ConfigSectionMap(section):
    dict1 = {};
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                #DebugPrint("skip: %s" % option)
                pass;
        except:
            #print("exception on %s!" % option)
            dict1[option] = None
    return dict1

settings = {};

for section in sections:
    settings[section] = ConfigSectionMap(section);