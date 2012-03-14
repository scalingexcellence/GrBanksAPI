**!!WARNING!!** Be really carefull with the passwords.cfg. Obviously this method of storing your bank account's credentials is very weak especially with Eurobank where a security token is not necessary for bank transfers. Use at your own risk! **DON'T share your files with friends, zip, distribute etc. and be careful with viruses**. Proactively a .gitignore rule has been added for you.

Quick start
----------------

Remove the .example from passwords.cfg.example and set your user/pass/acnt#. Adjust banks.py to your needs and you are ready to go.

You can merge the results of multiple accounts by adding them.

Examples
----------------

Some account examples:

    Eurobank(config)
    Eurobank('user','pass','account#')
    Eurobank(config,name='config_section_name')
    summary = Eurobank(config)+Alpha(config)
    summary.toCsv('summary.csv')
    
A complete example with multiple accounts and chaining:

    from ConfigParser import RawConfigParser
    import grbanks
    
    config = RawConfigParser()
    config.read('passwords.cfg')
    (grbanks.Eurobank(config)+grbanks.Alpha(config)+grbanks.Alpha(config,name="ALPHAB")).printp()

You can save to Excel format with the toCsv method. The Excel format support Greek characters. You can also perform arbitrary filtering, chaining and a custom formating

    (a+e).printp().toCsv("ae.csv")
    (a+e).printp().toCsv("ae.csv")
    (a+e).filter(grbanks.FILTER_POSITIVE).printp().toCsv("ae.csv")
    (a+e).format(grbanks.FORMAT_SUPERSIZE_ME).filter(grbanks.FILTER_POSITIVE).printp().toCsv("ae.csv")
    (a+e).format(grbanks.FORMAT_SUPERSIZE_ME).filter(lambda row: float(row['amount'])>300).printp().toCsv("ae.csv")

You might want to use gpg to encrypt your account info data:
    
    # See here on how to run gpg: http://www.madboa.com/geek/gpg-quickstart/
    # See here if you have problem generating random numbers: http://goo.gl/ecTsK

    # Create your keys:
    gpg --gen-key
    
    # Encode your keys:
    gpg -e -r "USERNAME" passwords.cfg
    rm passwords.cfg

    # Now decrypt on-the-fly and run:
    gpg -d --no-use-agent passwords.cfg.gpg | ./banks.py --stdin

The account# for Alpha Bank can be found here:

![Account number for Alpha Bank](https://github.com/scalingexcellence/GrBanksAPI/raw/master/doc/images/alpha.jpg "Account number for Alpha Bank")

and for Eurobank here:

![Account number for Eurobank](https://github.com/scalingexcellence/GrBanksAPI/raw/master/doc/images/eurob.jpg "Account number for Eurobank")
