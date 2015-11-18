#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from streamcorpus_pipeline._clean_visible import make_clean_visible

icq_examples = [['''  __     ______   ______               
         /\  __-.  /\ \/\ \   /\ "-./  \   /\  == \ /\  ___\icq:       615659311                     
         \ \ \/\ \ \ \ \_\ \  \ \ \-./\ \  \ \  _-/ \ \___  \ Email-&gt;           
          \ \____-  \ \__''', 615659311, ''],
['''                  
         Wholesale dealer VERIFIED DUMP SELLER BULK ONLY!!!            
         icq:       615659311        - yh: dumpspower@yahoo.com           
         DUMPS:           
                     
         Visa C''', 615659311, ''],
['''u need.            
         If you need more information or special conditions you can contact via icq:       615659311        or yahoo: dumpspower@yahoo.com            
         We will answer asap. The turn around time is    ''', 615659311, ''],
['''           
         Cantact US           
         Email: dumpspower@yahoo.com           
         ICQ:       615659311       
           
                     
         Wholesale dealer VERIFIED CVV SELLER       (       Uk,Eu Asia with bulk      )       , REAL GOOD SEL''', 615659311, ''],
['''sdso.ws cashoutcc.cc sellcvv.biz            
                     
         dumpspower@yahoo.com or ICQ       560874831                   
         Buzz me if u need any stuff ,I am good to my buyer.. poker game vegas casino gambling euro bets blac''', 560874831, ''],
[''' brand-shop.cc Silk Road            
                     
         Admin Site Marketplace Supports ICQ Number       668698740       
           
         carders.name cardersunion.net carders forum carding forums carders.name cvv dumps pin atm skimmer ss''', 668698740, ''],
['''issvpn.net carders.provhcteam.vn            
                     
         dumpspower@yahoo.com or ICQ       560874831        mn0g0.cc xtr3mehosting.co.cc validfullz.info Try2Check.me jackhack goldextreme.at.ua            
   ''', 560874831, ''],
['''dShop.ru - Best Cvv, Fulls &amp; Dumps Store           
         BEST QUALITY DUMPS! DUMPS TEACHER! ICQ:      171188       
           
         BABLO.CC - online cc shop       (       USA/EU/WORLD      )       
           
         Fresh Skimme''', 171188, ''],
[''' shop       (       USA/EU/WORLD      )       
           
         Fresh Skimmed World Wide Dumps! ICQ:      163444       
           
         DUMPSHOP.TV - ONLINE DUMP|CHECKER SHOP 24X7           
         BESTDUMPS.SU - ONLINE FRESH DUMP SHO''', 163444, ''],
['''terprise Quality Dumps and Service:      400983       
           
         Place for advertisement icq       819             -085       
           
         CARDSHOP.TV - ONLINE CC+CVV|CHECKER 24X7           
         DUMPS.PRO - VIRGIN STUFF FROM FIRST HAN''', 819085, ''],
['''fe.cc alli.ws           
         ADVERTISING BANNER OR LINE FREE -       350        USD PER MONTH. ICQ:       989             -737         gladyou.info carderprofit.cc Ta32 is good the software to            
                     
        ''', 989737, ''],
['''	                                             junior    
				     
			     
		
		
					    
				    ICQ     
				    
					266616226
					                                                                                         
				     
			     
		
		
					    
				    Интересы     
				    
					1C
				     
			     
		
        
					    
				    О себе     
				    ''', 266616226, ''],
['''  From:                              [[sell cvv(cc) good and fresh]]        
          
	        ***ICQ: 693462607     
     
===&gt; Hello all customer :     
     
- I am hacekker,good hacker , good seller , good stuff , sel''', 693462607, ''],
[''' info = 30$)     
     
- Asia = 15$ per 1 (fullz info = 30$)     
     
* Contact My:     
     
**ICQ : 693462607     
     
====&gt;Yahoo : boss.seller9     
     
====&gt;Email : boss.seller9@yahoo.com     
     
====&gt;Gm''', 693462607, ''],
['''mall : 1200$     
     
_Chip POS ingenico&amp;amigo : 700$     
     
****Contact My:     
     
**ICQ : 693462607     
     
====&gt;Yahoo : boss.seller9     
     
====&gt;Email : boss.seller9@yahoo.com     
     
====&gt;Gm''', 693462607, ''],
['''           
          
        _____ __ __ __ __ ______ ______      
/ __-. / /  / "-./  / ==  / ___icq: 615659311      
  /    _    -./    _-/  ___  Email-&gt;     
  ____-  _____  _  _  _ /_____ carderxp@yahoo.com     
 /''', 615659311, ''],
['''### ### ### ### ### ##########      
     
Wholesale dealer VERIFIED DUMP SELLER BULK ONLY!!!      
icq: 615659311 - yh: carderxp@yahoo.com     
DUMPS:     
      
Visa Classic, MasterCard Standard	      
10-50 pieces''', 615659311, ''],
['''st the stuff you need.      
If you need more information or special conditions you can contact via icq: 615659311 or yahoo: carderxp@yahoo.com      
We will answer asap. The turn around time is 3 hours. They will b''', 615659311, ''],
['''rs. They will be checked before delivery.     
     
Cantact US     
Email: carderxp@yahoo.com     
ICQ: 615659311     
     
     
&lt;HTML&gt;     
&lt;pre&gt;     
 _____ __ __ _ _______ ______ _____ _____      
 / ____| team2014''', 615659311, ''],
[''' | _ / ___  ym: cvvmasters@ymail.com     
| |___ V /  V /| | | |/ ____ ( / | | | |____| |   ____) | icq: 560874831      
 ______/ _/ |_| |_/_/ __| |_| |______|_| ______/      
     
      
     
      
=============== Cvv ''', 560874831, ''],
['''R TRADE..     
     
WHEN YOU READY TO BUY JUST PM US ON YAHOO msg YM: cvvmasters@ymail.com     
or ICQ 560874831     
     
     
     
Regards,      
CvvMASTERS Team     
Peace     
&lt;/pre&gt;     
&lt;/HTML&gt;     
     
     
    ''', 560874831, ''],
['''y Peru nhieu qua ai hot ko ne lsdso.ws cashoutcc.cc sellcvv.biz      
     
cvvmasters@ymail.com or ICQ 560874831      
Buzz me if u need any stuff, I am good to my buyer.. poker game vegas casino gambling euro bets blac''', 560874831, ''],
['''g forum, fraud money laundering brand-shop.cc Silk Road      
     
Admin Site Marketplace Supports ICQ Number 668698740     
carders.name cardersunion.net carders forum carding forums carders.name cvv dumps pin atm skimmer ss''', 668698740, ''],
[''' ccforsale.us ghostmarket.us swissvpn.net carders.provhcteam.vn      
     
cvvmasters@ymail.com or ICQ 560874831 mn0g0.cc xtr3mehosting.co.cc validfullz.info Try2Check.me jackhack goldextreme.at.ua      
     
zon''', 560874831, ''],
[''' ? en     
ValidShop.ru - Best Cvv, Fulls &amp; Dumps Store     
BEST QUALITY DUMPS! DUMPS TEACHER! ICQ:171188     
BABLO.CC - online cc shop (USA/EU/WORLD)     
Fresh Skimmed World Wide Dumps! ICQ:163444     
DUMPSH''', 171188, ''],
['''CHER! ICQ:171188     
BABLO.CC - online cc shop (USA/EU/WORLD)     
Fresh Skimmed World Wide Dumps! ICQ:163444     
DUMPSHOP.TV - ONLINE DUMP|CHECKER SHOP 24X7     
BESTDUMPS.SU - ONLINE FRESH DUMP SHOP     
SwipeDum''', 163444, ''],
['''SH DUMPS CCs - VLT.CC     
Enterprise Quality Dumps and Service:400983     
Place for advertisement icq 819-085     
CARDSHOP.TV - ONLINE CC+CVV|CHECKER 24X7     
DUMPS.PRO - VIRGIN STUFF FROM FIRST HANDS     
BEST AU''', 819085, ''],
['''rg wegot.in login cardrockcafe.cc alli.ws     
ADVERTISING BANNER OR LINE FREE - 350 USD PER MONTH. ICQ: 989-737 gladyou.info carderprofit.cc Ta32 is good the software to      
     
pebble is good but need the pe''', 989737, ''],
['''ds      
     
Best Shop EVER legitvendors.biz best prices. Pr0daem.Info Pr0daem.info Bestswipe.org ICQ: 555650782     
validshop.su chkr.biz eliteservices.name brand-shop.cc cartelgz.com binchecker.netne.net Cmaster4 Se''', 555650782, ''],
['''    
and balace      
CVV, PayPal, Bank logins, web services, RDP's, SOCKS5 cvvmasters@ymail.com or ICQ 560874831     
We sell Fullz cc cvv2 cvvs track bank PP login and dump all country SHOP contact US now!!! cvvmaster''', 560874831, ''],
['''edhacker     
     
------------Contact------------     
     
     
Yahoo ID : verifiedhacker     
ICQ : 573099662     
MAIL : verifiedhacker@yahoo.com     
Skype ID : cvvcharlie2014     
     
     
     
MAIL : verifie''', 573099662, 'cvvcharlie2014'],
['''     
     
     
-WHO NEED CONTACT FOR ME THROUGH:     
     
     
Yahoo ID : verifiedhacker     
ICQ : 573099662     
MAIL : verifiedhacker@yahoo.com     
Skype ID : cvvcharlie2014     
     
     
     
________----&g''', 573099662, 'cvvcharlie2014'],
[''' 
     
     
     
------------Contact------------     
     
     
Yahoo ID : verifiedhacker     
ICQ : 573099662     
MAIL : verifiedhacker@yahoo.com     
Skype ID : cvvcharlie2014     
     
     
     
     
     
==''', 573099662, 'cvvcharlie2014'],
['''AY     
     
     
------------Contact------------     
     
     
Yahoo ID : verifiedhacker     
ICQ : 573099662     
MAIL : verifiedhacker@yahoo.com     
Skype ID : cvvcharlie2014     
     
     
     
NO TEST     
N''', 573099662, 'cvvcharlie2014'],
['''ll_trade_50     
------------Contact------------     
     
     
Yahoo ID : buy_sell_trade_50     
ICQ : 573099662     
MAIL : buy_sell_trade_50@yahoo.com.vn     
Skype ID : cvvcharlie2014     
Hotmail : Hack_el_cvv@hotm''', 573099662, 'cvvcharlie2014'],
['''  
     
     
-WHO NEED CONTACT FOR ME THROUGH:     
     
     
Yahoo ID : buy_sell_trade_50     
ICQ : 573099662     
MAIL : buy_sell_trade_50@yahoo.com.vn     
Skype ID : cvvcharlie2014     
Hotmail : Hack_el_cvv@hotm''', 573099662, 'cvvcharlie2014'],
['''    
     
     
------------Contact------------     
     
     
Yahoo ID : buy_sell_trade_50     
ICQ : 573099662     
MAIL : buy_sell_trade_50@yahoo.com.vn     
Skype ID : cvvcharlie2014     
Hotmail : Hack_el_cvv@hotm''', 573099662, 'cvvcharlie2014'],
['''    
------------Contact------------     
     
     
     
Yahoo ID : buy_sell_trade_50     
     
ICQ : 573099662     
     
MAIL : buy_sell_trade_50@yahoo.com.vn     
     
Skype ID : cvvcharlie2014     
     
Hotmail : Hack''', 573099662, 'cvvcharlie2014'],
['''Having experience in information technology in 6 years     
- If you need CVV please contact me via ICQ : 697622270     
- I'm seller best and alway sell CC fresh with hight balance.     
- And i have software do bug accoun''', 697622270, ''],
[''' good customers and will be long-term cooperation     
     
     
gmail: neelluna87@gmail.com     
ICQ : 697622270     
     
PRICE LIST :     
     
Us (Visa, Master) = $4 per 1     
Us (Amex, Discover) = $8 per 1     
Us wit''', 697622270, ''],
['''ecipient information     
     
* Contact me via Adress     
     
gmail: neelluna87@gmail.com     
ICQ : 697622270     
     
--------- Dumps / Track 1&amp;2 For Price ----------     
     
* Dumps, Tracks 1&amp;2 US = $50 per 1     
* ''', 697622270, ''],
['''ess . Don't Ask For Small Bussiness     
CONTACT INFO :     
     
gmail: neelluna87@gmail.com     
ICQ : 697622270     
     
... make money for you, thank you ------welcome you ...          
                  
               ''', 697622270, ''],
['''Having experience in information technology in 6 years     
- If you need CVV please contact me via ICQ : 697622270     
- I'm seller best and alway sell CC fresh with hight balance.     
- And i have software do bug accoun''', 697622270, ''],
[''' good customers and will be long-term cooperation     
     
     
gmail: neelluna87@gmail.com     
ICQ : 697622270     
     
PRICE LIST :     
     
Us (Visa, Master) = $4 per 1     
Us (Amex, Discover) = $8 per 1     
Us wit''', 697622270, ''],
['''ecipient information     
     
* Contact me via Adress     
     
gmail: neelluna87@gmail.com     
ICQ : 697622270     
     
--------- Dumps / Track 1&amp;2 For Price ----------     
     
* Dumps, Tracks 1&amp;2 US = $50 per 1     
* ''', 697622270, ''],
['''ess . Don't Ask For Small Bussiness     
CONTACT INFO :     
     
gmail: neelluna87@gmail.com     
ICQ : 697622270     
     
... make money for you, thank you ------welcome you ...          
                  
               ''', 697622270, ''],
['''                                            
          
        Hello, CVV is my best for you      
icq: 699817352 I'm a sell: CC, CVV U.S., UK, CA, EURO, AU, Italian, Japanese, French, ... all      
cc.      
Fullz''', 699817352, ''],
[''' you in a long time, thanks!      
no scamer no spamer      
thanks!      
Please contact me:      
icq: 699817352     
gmail: good.cheap27@gmail.com          
                  
                              
        42''', 699817352, ''],
['''me NOW for more information :     
     
------------------------------------------     
===&gt; My ICQ : 665549487      
===&gt; My ID E-mail : greatseller79@gmail.com     
------------------------------------------     
''', 665549487, ''],
['''05, and much pin other     
     
.I only have 1 Mail : greatseller79@gmail.com     
 I only have 1 ICQ : 665549487     
     
If You Need CVV or ANY TOOLS, Please contact me NOW for more information :     
     
--------------''', 665549487, ''],
['''me NOW for more information :     
     
------------------------------------------     
===&gt; My ICQ : 665549487      
===&gt; My ID E-mail : greatseller79@gmail.com     
------------------------------------------     
''', 665549487, ''],
['''me NOW for more information :     
     
------------------------------------------     
===&gt; My ICQ : 665549487      
===&gt; My ID E-mail : greatseller79@gmail.com     
------------------------------------------     
''', 665549487, ''],
['''few, little cc to test     
4 . I only have 1 Mail : greatseller79@gmail.com     
5 . I only have 1 ICQ : 665549487     
     
If You Need CVV or ANY TOOLS, Please contact me NOW for more information :     
     
--------------''', 665549487, ''],
['''me NOW for more information :     
     
------------------------------------------     
===&gt; My ICQ : 665549487      
===&gt; My ID E-mail : greatseller79@gmail.com     
------------------------------------------     
''', 665549487, ''],
['''nd will be long-term cooperation.     
     
*** My ID Gmail : sellccvno1@gmail.com      
     
*** ICQ : 633448267     
     
*** Skype : new.exchanger     
     
... TRANSFER WESTERN UNION SERVICES ...     
     
     
*** Tr''', 633448267, 'new.exchanger'],
['''ange if cc not good or dont work.     
     
*** My ID Gmail : sellccvno1@gmail.com      
     
*** ICQ : 633448267     
     
*** Skype : new.exchanger     
     
--------- Exchange ------------     
     
- 100 pm, wmz = $105''', 633448267, 'new.exchanger'],
['''---------------------------------     
     
*** My ID Gmail : sellccvno1@gmail.com      
     
*** ICQ : 633448267     
     
*** Skype : new.exchanger     
     
... See you soon ...          
                  
             ''', 633448267, 'new.exchanger'],
['''nd will be long-term cooperation.     
     
*** My ID Gmail : sellccvno1@gmail.com      
     
*** ICQ : 633448267     
     
*** Skype : new.exchanger     
     
... TRANSFER WESTERN UNION SERVICES ...     
     
     
*** Tr''', 633448267, 'new.exchanger'],
['''ange if cc not good or dont work.     
     
*** My ID Gmail : sellccvno1@gmail.com      
     
*** ICQ : 633448267     
     
*** Skype : new.exchanger     
     
--------- Exchange ------------     
     
- 100 pm, wmz = $105''', 633448267, 'new.exchanger'],
['''---------------------------------     
     
*** My ID Gmail : sellccvno1@gmail.com      
     
*** ICQ : 633448267     
     
*** Skype : new.exchanger     
     
... See you soon ...          
                  
             ''', 633448267, 'new.exchanger'],
['''nd will be long-term cooperation.     
     
*** My ID Gmail : sellccvno1@gmail.com      
     
*** ICQ : 633448267     
     
*** Skype : new.exchanger     
     
... TRANSFER WESTERN UNION SERVICES ...     
     
     
*** Tr''', 633448267, 'new.exchanger'],
['''ange if cc not good or dont work.     
     
*** My ID Gmail : sellccvno1@gmail.com      
     
*** ICQ : 633448267     
     
*** Skype : new.exchanger     
     
--------- Exchange ------------     
     
- 100 pm, wmz = $105''', 633448267, 'new.exchanger'],
['''---------------------------------     
     
*** My ID Gmail : sellccvno1@gmail.com      
     
*** ICQ : 633448267     
     
*** Skype : new.exchanger     
     
... See you soon ...          
                  
             ''', 633448267, 'new.exchanger'],
[''' ID : real_seller_cvv     
Email : real_seller_cvv@yahoo.com     
msn : cvvcharlie@hotmail.com     
ICQ : 554143381     
Skype ID : cvvcharlie2014     
Gmail : verifiedhacker50@gmail.com     
FACEBOOK : bigger seller     ''', 554143381, 'cvvcharlie2014'],
[''' ID : real_seller_cvv     
Email : real_seller_cvv@yahoo.com     
msn : cvvcharlie@hotmail.com     
ICQ : 554143381     
Skype : cvvcharlie2014     
Gmail : cvvcharlie@gmail.com     
FACEBOOK : bigger seller     
     
  ''', 554143381, 'cvvcharlie2014'],
['''il : real_seller_cvv@yahoo.com     
FACEBOOK : bigger seller     
msn : cvvcharlie@hotmail.com     
ICQ : 554143381     
Skype : cvvcharlie2014     
Gmail : verifiedhacker50@gmail.com     
     
     
     
I USE PM ACC (''', 554143381, 'cvvcharlie2014'],
['''D : super_seller_cvv     
Email : super_seller_cvv@yahoo.com     
msn : cvvcharlie@hotmail.com     
ICQ : 554143381     
Skype ID : cvvcharlie2014     
Gmail : verifiedhacker50@gmail.com     
FACEBOOK : bigger seller     ''', 554143381, 'cvvcharlie2014'],
['''D : super_seller_cvv     
Email : super_seller_cvv@yahoo.com     
msn : cvvcharlie@hotmail.com     
ICQ : 554143381     
Skype ID : cvvcharlie2014     
Gmail : verifiedhacker50@gmail.com     
FACEBOOK : bigger seller     ''', 554143381, 'cvvcharlie2014'],
['''ID : super_seller_cv     
Email : super_seller_cvv@yahoo.com     
msn : cvvcharlie@hotmail.com     
ICQ : 554143381     
Skype ID : cvvcharlie2014     
Gmail : verifiedhacker50@gmail.com     
FACEBOOK : bigger seller     ''', 554143381, 'cvvcharlie2014'],
['''me NOW for more information :     
     
------------------------------------------     
===&gt; My ICQ : 665549487      
===&gt; My ID E-mail : greatseller79@gmail.com     
------------------------------------------     
''', 665549487, ''],
['''few, little cc to test     
4 . I only have 1 Mail : greatseller79@gmail.com     
5 . I only have 1 ICQ : 665549487     
If You Need CVV or ANY TOOLS, Please contact me NOW for more information :     
     
--------------''', 665549487, ''],
['''me NOW for more information :     
     
------------------------------------------     
===&gt; My ICQ : 665549487      
===&gt; My ID E-mail : greatseller79@gmail.com     
------------------------------------------     
''', 665549487, ''],
['''me NOW for more information :     
     
------------------------------------------     
===&gt; My ICQ : 665549487      
===&gt; My ID E-mail : greatseller79@gmail.com     
------------------------------------------     
''', 665549487, ''],
['''few, little cc to test     
4 . I only have 1 Mail : greatseller79@gmail.com     
5 . I only have 1 ICQ : 665549487     
If You Need CVV or ANY TOOLS, Please contact me NOW for more information :     
     
--------------''', 665549487, ''],
['''me NOW for more information :     
     
------------------------------------------     
===&gt; My ICQ : 665549487      
===&gt; My ID E-mail : greatseller79@gmail.com     
------------------------------------------     
''', 665549487, ''],
['''                                                                                                   #ICQ : 78277777 =&gt; SELL Cvv2, Cc GOOD FRESH CHEAP/ Dumps Track 1 &amp; 2/ Transfer Wu                            ''', 78277777, ''],
['''                                                                                                    ICQ: 691570706 --&gt; Sell cc/transfer WU/Bank login/Paypal/Dump Track 1 or 2                                        ''', 691570706, ''],
['''                                                                                                    ICQ: 691570706 --&gt; Transfer WU/Sell Cvv/Bank login/Paypal/Dump Track 1 or 2                                       ''', 691570706, ''],
['''  __     ______   ______               
         /\  __-.  /\ \/\ \   /\ "-./  \   /\  == \ /\  ___\icq: 615659311              
         \ \ \/\ \ \ \ \_\ \  \ \ \-./\ \  \ \  _-/ \ \___  \ Email-&gt;           
          \ \____-  \ \__''', 615659311, ''],
['''                  
         Wholesale dealer VERIFIED DUMP SELLER BULK ONLY!!!            
         icq: 615659311 - yh: dumpspower@yahoo.com           
         DUMPS:           
                     
         Visa C''', 615659311, ''],
['''u need.            
         If you need more information or special conditions you can contact via icq: 615659311 or yahoo: dumpspower@yahoo.com            
         We will answer asap. The turn around time is 3 h''', 615659311, ''],
['''           
         Cantact US           
         Email: dumpspower@yahoo.com           
         ICQ: 615659311           
                     
         Wholesale dealer VERIFIED CVV SELLER (Uk,Eu Asia with bulk), REAL GOOD SELLER LEGIT VERIFIED DUMPS S''', 615659311, ''],
['''sdso.ws cashoutcc.cc sellcvv.biz            
                     
         dumpspower@yahoo.com or ICQ 560874831            
         Buzz me if u need any stuff ,I am good to my buyer.. poker game vegas casino gambling euro bets blac''', 560874831, ''],
[''' brand-shop.cc Silk Road            
                     
         Admin Site Marketplace Supports ICQ Number 668698740           
         carders.name cardersunion.net carders forum carding forums carders.name cvv dumps pin atm skimmer ss''', 668698740, ''],
['''issvpn.net carders.provhcteam.vn            
                     
         dumpspower@yahoo.com or ICQ 560874831 mn0g0.cc xtr3mehosting.co.cc validfullz.info Try2Check.me jackhack goldextreme.at.ua            
   ''', 560874831, ''],
['''dShop.ru - Best Cvv, Fulls &amp; Dumps Store           
         BEST QUALITY DUMPS! DUMPS TEACHER! ICQ:171188           
         BABLO.CC - online cc shop (USA/EU/WORLD)           
         Fresh Skimmed World Wide Dumps! ICQ:163''', 171188, ''],
['''       BABLO.CC - online cc shop (USA/EU/WORLD)           
         Fresh Skimmed World Wide Dumps! ICQ:163444           
         DUMPSHOP.TV - ONLINE DUMP|CHECKER SHOP 24X7           
         BESTDUMPS.SU - ONLINE FRESH DUMP SHO''', 163444, ''],
['''  
         Enterprise Quality Dumps and Service:400983           
         Place for advertisement icq 819-085           
         CARDSHOP.TV - ONLINE CC+CVV|CHECKER 24X7           
         DUMPS.PRO - VIRGIN STUFF FROM FIRST HAN''', 819085, ''],
['''in cardrockcafe.cc alli.ws           
         ADVERTISING BANNER OR LINE FREE - 350 USD PER MONTH. ICQ: 989-737  gladyou.info carderprofit.cc Ta32 is good the software to            
                     
        ''', 989737, ''],
['''     
         Best Shop EVER legitvendors.biz best prices. Pr0daem.Info Pr0daem.info Bestswipe.org ICQ: 555650782           
         validshop.su chkr.biz eliteservices.name brand-shop.cc cartelgz.com binchecker.netne.net Cmaster4 Se''', 555650782, ''],
['''            
         CVV, PayPal, Bank logins, web services, RDP's, SOCKS5 dumpspower@yahoo.com or ICQ 560874831           
         We sell Fullz cc cvv2 cvvs track bank PP login and dump all country SHOP contact US now!!! dumpspowe''', 560874831, ''],
['''nnect it to the 3G-4G network      
Starting AMOUNT OF upload is  200$  to 1000$     
Contact us on ICQ: 674828332
								    

								       
									     
																			      

									     
										Anonymous
										•
										26 Nov 2014, 19:37:33 UTC
									      
								        
							  ''', 674828332, ''],
['''   
    Связь с авторами:     
                
  
                                                 ICQ:    165-638-224    
    
  
                                                   Skype:    br110878kdl    
    
  
                                                   E-mail:        ''', 165638224, 'br110878kdl'],
['''               3230        Имя:     Max        Пол: Мужской    День рождения:     1980-12-28        Icq:     266616226                                                                              Страна:     Россия        Город:     Омск        Рост:     176        Вес:     63        Модель моби''', 266616226, ''],

[make_clean_visible(u'''</div> Icq: 266616226'''), 266616226, ''],
['<title>hello ICQ.com</title>					UIN <span data-user-profile="other_profile_uin">100001</span>', 100001, ''],
[open(os.path.join(os.path.dirname(__file__), 'data/galli.ru.html')).read(), 266616226, ''],
]
