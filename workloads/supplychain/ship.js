'use strict';

const rand = require('./random');
const seeds = require('./seeds.json');
const GLN = require('./gln');
const getParameters = require('./getParameters');

class ship {

    static get() {

    let args;
    let standardDerivation = getParameters.keyPickerType();
    let randomAccessKey = rand.randomIndex(seeds.allSSCC.length, standardDerivation);
    while (seeds.allSSCC[randomAccessKey] === undefined) {
        randomAccessKey = rand.randomIndex(seeds.allSSCC.length, standardDerivation);
    }
    let ssccKey = seeds.allSSCC[randomAccessKey];

    randomAccessKey = rand.randomIndex(seeds.allLsp.length, standardDerivation);
    while (seeds.allLsp[randomAccessKey] === undefined) {
        randomAccessKey = rand.randomIndex(seeds.allLsp.length, standardDerivation);
    }
    let newLSPNameString = seeds.allLsp[randomAccessKey].name;
    //console.info(newLSPNameString);
    let gln = new GLN(seeds.allLsp[randomAccessKey].gln.gs1CompanyPrefix, seeds.allLsp[randomAccessKey].gln.locationReference);
    let newLSPGlnString = gln.toString();

	    let invkIdent = rand.getClient()
            console.log("invkIdent", invkIdent);
            let targetOrg = rand.getEndorsers()
            console.log("targetOrg", targetOrg);

            args = {
                contractId: 'supplychain',
                contractVersion: 'v1',
                contractFunction: 'ship',
                contractArguments: [ssccKey, newLSPNameString, newLSPGlnString],
                targetOrganizations: targetOrg,
                invokerIdentity: invkIdent,
                timeout: 30
            };


            return args;

        }
}

module.exports = ship;

