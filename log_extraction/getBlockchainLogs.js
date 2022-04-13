
//TODO: Automate these steps.
/*
Execute the following steps before running this script:

1. Create/Copy/Edit the connectionprofile.yaml to match the Fabric network configuration. For example:  
cp /home/ubuntu/HyperLedgerLab-2.0_Extended/caliper/caliper-config/templates/networkConfig.yaml /home/ubuntu/BlockOptR/log_extraction/connectionprofile.yaml

2. Edit connectionprofile.yaml such that there is only one client as shown below:
client:
      organization: Org1
      credentialStore:
        path: /tmp/1615470564-cred/org1
        cryptoStore:
          path: /tmp/1615470564-crypto/org1
      clientPrivateKey:
        path: /home/ubuntu/HyperLedgerLab-2.0_Extended/inventory/blockchain/fabric-config/crypto-config/peerOrganizations/org1/users/User1@org1/msp/keystore/priv_sk
      clientSignedCert:
        path: /home/ubuntu/HyperLedgerLab-2.0_Extended/inventory/blockchain/fabric-config/crypto-config/peerOrganizations/org1/users/User1@org1/msp/signcerts/User1@org1-cert.pem
	
	
3. mkdir data if it does not exist. rm data/* if it exists.
*/


'use strict';

const fs = require('fs');
const FabricClient = require('fabric-client');



async function setClient() {
	 
	let client =  FabricClient.loadFromConfig('./log_extraction/connectionprofile.yaml')
	await client.initCredentialStores()
	        .then(async (nothing) => {
			await client.setUserContext({username:'admin', password:'adminpw'})
         			.then(async (admin) => {
				const channel = client.getChannel();
				let blockchaininfo = await channel.queryInfo();
				let blockchainheight = blockchaininfo.height;
				blockchainheight = blockchainheight|0;
				//The complete blockchain is parsed
				for (let index = 0; index < blockchainheight; index++) {
    					var fileName = "./log_extraction/data/" + index + ".json";
					var jsonstr = "";
					try {
						//Blocks are queried from the blockchain
						jsonstr = JSON.stringify((await channel.queryBlock(index)), null, 4)
					}
					catch(e) {
						console.log("CAUGHT JSON LENGTH EXCEPTION")
					}
					//Blocks are written to the filesystem
    					fs.writeFile(
                          				fileName,
			                                jsonstr,
                  					function (err) {
                              						if (err) {
                                 						console.error('Saving BLOCK failed');
                              							}
                          						}
                    						);
                		}



          			return channel;

							
							
				})
						
						
		})



}

setClient()
  .then((channel) => { 
	  console.log('Client setup successful')

  })
  .then(() => { console.log('Client setup complete')});

