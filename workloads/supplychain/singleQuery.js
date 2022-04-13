'use strict';

const rand = require('./random');
const seeds = require('./seeds.json');
const getParameters = require('./getParameters');
class singleQuery {

    static get() {

    let args;
    let standardDerivation = getParameters.keyPickerType();
    let randomAccessKey = rand.randomIndex(seeds.allSSCC.length, standardDerivation);
    let ssccKey = seeds.allSSCC[randomAccessKey].toString();

	    let invkIdent = rand.getClient()
            console.log("invkIdent", invkIdent);
            let targetOrg = rand.getEndorsers()
            console.log("targetOrg", targetOrg);

            args = {
                contractId: 'supplychain',
                contractVersion: 'v1',
                contractFunction: 'queryLogisticUnit',
                contractArguments: [ssccKey],
                targetOrganizations: targetOrg,
                invokerIdentity: invkIdent,
                timeout: 30
            };



            return args;

        }
}

module.exports = singleQuery;

