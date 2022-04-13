'use strict';

const rand = require('./random');
const seeds = require('./seeds.json');
const getParameters = require('./getParameters');

class queryStock {

    static get() {

    let args;
    let standardDerivation = getParameters.keyPickerType();

    let randomAccessKey = rand.randomIndex(seeds.allLsp.length, standardDerivation);
    let lsp = seeds.allLsp[randomAccessKey];
    let lspName = lsp !== undefined ? lsp.name : 'LSPA';

	    let invkIdent = rand.getClient()
            console.log("invkIdent", invkIdent);
            let targetOrg = rand.getEndorsers()
            console.log("targetOrg", targetOrg);

            args = {
                contractId: 'supplychain',
                contractVersion: 'v1',
                contractFunction: 'queryStock',
                contractArguments: [lspName],
                targetOrganizations: targetOrg,
                invokerIdentity: invkIdent,
                timeout: 30
            };


            return args;

        }
}

module.exports = queryStock;

