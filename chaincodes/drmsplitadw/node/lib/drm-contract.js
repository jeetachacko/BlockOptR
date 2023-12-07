/*
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const { Contract } = require('fabric-contract-api');

const seeds = require('./seeds.json');

const Utils = require('./utils');
const RoyaltyManagement = require('./royaltyManagement');
const Metadata = require('./metadata');

class DrmContract extends Contract {

    async init(ctx) {
        console.info('DRM Contract initialized');
    }

    async doNothing(ctx) {
        console.info('============= DoNothing Function ===========');
    }

    async InitLedger(ctx) {
        console.info('============= START : Initialize Ledger ===========');
        for (let [key, value] of Object.entries(seeds.allUploadedArtwork)) {
            const val = JSON.parse(value);
            const asset = Metadata.fromJSON(val);
            console.info(`${asset}`);
            const buffer = Buffer.from(JSON.stringify(asset));
            await ctx.stub.putState(key, buffer);
        }

        for (let [key, value] of Object.entries(seeds.allUploadedRoyaltyManagement)) {
            const val = JSON.parse(value);
            const asset = RoyaltyManagement.fromJSON(val);
            console.info(`${asset}`);
            const buffer = Buffer.from(JSON.stringify(asset));
            await ctx.stub.putState(key, buffer);
        }
	    let chaincodeResponse = await ctx.stub.invokeChaincode("drmsplitbdw", ["InitLedger"], ctx.stub.getChannelID());
        console.info('============= START : Initialize Ledger ===========');
    }

    async create(ctx, metadataId, metadata, royaltyManagementId, royaltyManagement) {
        let buffer = await ctx.stub.getState(metadataId);
        if (!(!!buffer && buffer.length > 0)) {

            const metadataAsset = Metadata.fromJSON(JSON.parse(metadata));
            console.info(JSON.stringify(metadataAsset));
            const metadataBuffer = Buffer.from(JSON.stringify(metadataAsset));
            await ctx.stub.putState(metadataId, metadataBuffer);

            const royaltyManagementAsset = RoyaltyManagement.fromJSON(JSON.parse(royaltyManagement));
            console.info(JSON.stringify(royaltyManagementAsset));
            const royaltyManagementBuffer = Buffer.from(JSON.stringify(royaltyManagementAsset));
            await ctx.stub.putState(royaltyManagementId, royaltyManagementBuffer);
	const chaincodeResponse = await ctx.stub.invokeChaincode("drmsplitbdw", ["create", metadataId, metadata, royaltyManagementId, royaltyManagement], ctx.stub.getChannelID());

        }
    }

    async play(ctx, artWorkId) {
        const metadataBuffer = await ctx.stub.getState(artWorkId);
        const metadata = Utils.handleStateQueryResult(metadataBuffer);
	console.info('metadata');
        console.info(metadata);

        let royaltyManagementBuffer = await ctx.stub.getState(metadata.royaltyManagementId);
        let royaltyManagementAsset = Utils.handleStateQueryResult(royaltyManagementBuffer);

        //royaltyManagementAsset.incrementPlayCount();

        //royaltyManagementBuffer = Buffer.from(JSON.stringify(royaltyManagementAsset));
        //await ctx.stub.putState(metadata.royaltyManagementId, royaltyManagementBuffer);
	const name = metadata.royaltyManagementId
        const op = "+"
        const increment = String(1)
        const txid = await ctx.stub.getTxID()
        const compositeIndexName = "varName~op~value~txID"
        let value = [name, op, increment, txid]
        const compositeKey = await ctx.stub.createCompositeKey(compositeIndexName, value)
        const compositePutErr = await ctx.stub.putState(compositeKey, "NULL")

        console.info('compositePutErr');
        return compositePutErr
    }

    async calcRevenue(ctx, ipiName) {

	    console.info('In calcRevenue');
        let allRoyaltyFee = 0;

        let queryString = {};

        queryString.selector = {
            docType: 'royaltyManagement',
            allRightHolder: {
                $elemMatch: { ipiName: ipiName }
            }
        };
	    console.info('Before try');
	    console.info(queryString);

        try {
		console.info('in try');

        let resultsIterator = await ctx.stub.getQueryResult(JSON.stringify(queryString));

		console.info('resultsiterator');
        const allResult = await Utils.handleStateQueryIterator(resultsIterator);
                var t = 0


	console.info('allResult.length');
		console.info(allResult.length);
        for(var j=0; j<allResult.length; j++) {

        var royaltyManagementAsset=allResult[j]

        const deltaResultsIterator = await ctx.stub.getStateByPartialCompositeKey("varName~op~value~txID", allResult[j])
        t=t+1

        let finalVal = 0
        var i
        for (i = 0; i<deltaResultsIterator.length; i++) {
		console.info('deltaResultsIterator.length');
		console.info(deltaResultsIterator.length);

                keyParts = await ctx.stub.splitCompositeKey(deltaResultsIterator[i].Key)

                //operation = keyParts[1]
                valueStr = keyParts[2]

                value = parseFloat(valueStr)

                /*switch(operation) {
                case "+":
                        finalVal += value
                case "-":
                        finalVal -= value
                default:
                        //return shim.Error(fmt.Sprintf("Unrecognized operation %s", operation))
                }*/
                finalVal += value

                // PRUNE: Delete the row from the ledger
                let deltaRowDelErr = ctx.stub.delState(deltaResultsIterator[i].Key)
                //if deltaRowDelErr != nil {
                //      return shim.Error(fmt.Sprintf("Could not delete delta row: %s", deltaRowDelErr.Error()))
                //}



                //UPDATE new aggregated value
                const name = keyParts[0]
                const op = "+"
                const increment = String(finalVal)
                const txid = await ctx.stub.getTxID()
                const compositeIndexName = "varName~op~value~txID"
                let value = [name, op, increment, txid]
                const compositeKey = await ctx.stub.createCompositeKey(compositeIndexName, value)
                const compositePutErr = await ctx.stub.putState(compositeKey, "NULL")

                console.info('updated');



        }

        let playCount = finalVal
                const share = royaltyManagementAsset.allRightHolder.filter(rightHolder => rightHolder.ipiName === ipiName)[0].share;

            const royaltyFee =
                playCount *
                royaltyManagementAsset.perPlayRoyalty *
                share;

            allRoyaltyFee += royaltyFee;
        }
        //});

        console.info(`${ipiName} aggregated revenue ${allRoyaltyFee} from ${allResult.length} art works`);

        return { ipiName: allRoyaltyFee };

        } catch (error) {
                console.error(error);
        }
    }

}

module.exports = DrmContract;
