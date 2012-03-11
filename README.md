Just see the banks.py for an example of use. Remove the .example from passwords.cfg.example, set your user/pass for the banks, hack banks.py and you are ready to go. You can merge the results of multiple accounts by adding them. Account examples:

    Eurobank(config)
    Eurobank('user','pass','account#')
    Eurobank(config,name='config_section_name')
    summary = Eurobank(config)+Alpha(config)
    summary.toCsv('summary.csv')
    
A complete example with multiple accounts and chaining:

    from alpha import Alpha
    from eurobank import Eurobank
    from ConfigParser import RawConfigParser
    
    config = RawConfigParser()
    config.read('passwords.cfg')
    (Eurobank(config)+Alpha(config)+Alpha(config,name="ALPHAB")).toCsv('summary.csv').printp()

You can save to Excel format with the toCsv method. The Excel format support Greek characters.

**!!WARNING!!** Be really carefull with the passwords.cfg. Obviously this method of storing your bank account #'s is very weak especially with Eurobank where key is not necessary for bank transfers. !! Use at your own risk, **DON'T share your files with friends, zip, distribute etc. and be careful with viruses**. Proactively a .gitignore rule has been added for you.

The account# for Alpha Bank can be found here:

![Account number for Alpha Bank](https://github.com/scalingexcellence/GrBanksAPI/raw/master/doc/images/alpha.jpg "Account number for Alpha Bank")

and for Eurobank here:

![Account number for Eurobank](https://github.com/scalingexcellence/GrBanksAPI/raw/master/doc/images/eurob.jpg "Account number for Eurobank")
