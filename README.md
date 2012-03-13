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

    from alpha import Alpha
    from eurobank import Eurobank
    from ConfigParser import RawConfigParser
    
    config = RawConfigParser()
    config.read('passwords.cfg')
    (Eurobank(config)+Alpha(config)+Alpha(config,name="ALPHAB")).toCsv('summary.csv').printp()

You can save to Excel format with the toCsv method. The Excel format support Greek characters.

If you would like to avoid using files (for security reasons) you might find the following examples useful:

    
    # See here on how to run gpg: http://www.madboa.com/geek/gpg-quickstart/
    # See here if you have problem generating random numbers: http://www.howtoforge.com/helping-the-random-number-generator-to-gain-enough-entropy-with-rng-tools-debian-lenny

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
