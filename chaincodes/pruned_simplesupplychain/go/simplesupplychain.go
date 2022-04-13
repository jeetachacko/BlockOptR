/*
SPDX-License-Identifier: Apache-2.0
*/

package main

import (
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
	contractapi.Contract
}

func main() {

        chaincode, err := contractapi.NewChaincode(new(SmartContract))

        if err != nil {
                fmt.Printf("Error create supplychain chaincode: %s", err)
        }

        if err := chaincode.Start(); err != nil {
                fmt.Printf("Error starting supplychain chaincode: %s", err.Error())
        }
}

func (s *SmartContract) Init(ctx contractapi.TransactionContextInterface) error {
        return nil
}


type Product struct {
	Id   string `json:"id"`
	Date  string `json:"date"`
	Source string `json:"source"`
	Destination  string `json:"destination"`
	Status string `json:"status"` //nil: defailt, 0:ASN pushed, 1:Shipped, 2:Unloaded
}

type QueryResult struct {
	Key    string `json:"Key"`
	Record *Product
}

type AuditInfo struct {
        AuditKey    string `json:"AuditKey"`
        CriticalList []string
}


func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {

	locations := []string{"A", "B", "C", "D"}
	for i := 0; i < 20000; i++ {
		product := Product{Id: strconv.Itoa(i), Date: "", Source: locations[i % 3], Destination: locations[i % 3], Status: "nil"}
		productAsBytes, _ := json.Marshal(product)
		err := ctx.GetStub().PutState(strconv.Itoa(i), productAsBytes)
		if err != nil {
                        return fmt.Errorf("Failed to put to world state. %s", err.Error())
                }

	}

	return nil
}

func (s *SmartContract) UpdateAuditInfo(ctx contractapi.TransactionContextInterface, key string, auditkey string) error {

	productAsBytes, err := ctx.GetStub().GetState(key)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if productAsBytes == nil {
                return fmt.Errorf("%s does not exist", key)
        }

	 product := new(Product)
        _ = json.Unmarshal(productAsBytes, product)

	auditAsBytes, err := ctx.GetStub().GetState(auditkey)
	if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if auditAsBytes == nil {
		arrproduct := []string{product.Id}
		auditinfo := AuditInfo{AuditKey: auditkey, CriticalList: arrproduct}
		auditAsBytes, _ := json.Marshal(auditinfo)
		err := ctx.GetStub().PutState(auditkey, auditAsBytes)
		if err != nil {
                        return fmt.Errorf("Failed to put to world state. %s", err.Error())
                }

        }
	auditinfo := new(AuditInfo)
	_ = json.Unmarshal(auditAsBytes, auditinfo)
	auditinfo.CriticalList = append(auditinfo.CriticalList, product.Id)
	auditAsBytes, _ = json.Marshal(auditinfo)
	return ctx.GetStub().PutState(auditkey, auditAsBytes)

}

func (s *SmartContract) PushASN(ctx contractapi.TransactionContextInterface, key string, date string, destination string) error {

	productAsBytes, err := ctx.GetStub().GetState(key)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if productAsBytes == nil {
                return fmt.Errorf("%s does not exist", key)
        }

        product := new(Product)
        _ = json.Unmarshal(productAsBytes, product)

        product.Date = date
	product.Destination = destination
	product.Status = "0"

        productAsBytes, _ = json.Marshal(product)

        return ctx.GetStub().PutState(key, productAsBytes)
}

func (s *SmartContract) QueryASN(ctx contractapi.TransactionContextInterface, key string) (*Product, error) {
	productAsBytes, err := ctx.GetStub().GetState(key)

	if err != nil {
		return nil, fmt.Errorf("Failed to read from world state. %s", err.Error())
	}

	if productAsBytes == nil {
		return nil, fmt.Errorf("%s does not exist", key)
	}

	product := new(Product)
	_ = json.Unmarshal(productAsBytes, product)

	if product.Status != "0" {

		return nil, fmt.Errorf("No ASN for %s", key)
		//fmt.Print("No ASN for %s", key)
	}
	return product, nil
}

func (s *SmartContract) Ship(ctx contractapi.TransactionContextInterface, key string) error {

        productAsBytes, err := ctx.GetStub().GetState(key)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if productAsBytes == nil {
                return fmt.Errorf("%s does not exist", key)
        }

        product := new(Product)
        _ = json.Unmarshal(productAsBytes, product)

	if(product.Status == "1") {
		return fmt.Errorf("%s is already shipped", key)

	}
        if(product.Status != "0") {
                return fmt.Errorf("No ASN sent for %s", key)
                //fmt.Print("No ASN sent for %s", key)
                //return nil

        }


	product.Status = "1"
	productAsBytes, _ = json.Marshal(product)
	return ctx.GetStub().PutState(key, productAsBytes)

}

func (s *SmartContract) Unload(ctx contractapi.TransactionContextInterface, key string) error {

        productAsBytes, err := ctx.GetStub().GetState(key)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if productAsBytes == nil {
                return fmt.Errorf("%s does not exist", key)
        }

        product := new(Product)
        _ = json.Unmarshal(productAsBytes, product)

        if(product.Status == "2") {

                return fmt.Errorf("%s is already unloaded", key)
                //fmt.Print("%s is already unloaded", key)
                //return nil
        }
	if(product.Status != "1") {
                return fmt.Errorf("%s is not shipped", key)
                //fmt.Print("%s is not shipped", key)
                //return nil

        }

	product.Status = "2"
	product.Source = product.Destination
        productAsBytes, _ = json.Marshal(product)
        return ctx.GetStub().PutState(key, productAsBytes)
}


func (s *SmartContract) QueryProducts(ctx contractapi.TransactionContextInterface, startKey string, endKey string) ([]QueryResult, error) {

	resultsIterator, err := ctx.GetStub().GetStateByRange(startKey, endKey)

	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	results := []QueryResult{}

	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()

		if err != nil {
			return nil, err
		}

		product := new(Product)
		_ = json.Unmarshal(queryResponse.Value, product)

		queryResult := QueryResult{Key: queryResponse.Key, Record: product}
		results = append(results, queryResult)
	}

	return results, nil
}


/*
func main() {

	chaincode, err := contractapi.NewChaincode(new(SmartContract))

	if err != nil {
		fmt.Printf("Error create supplychain chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting supplychain chaincode: %s", err.Error())
	}
}*/
