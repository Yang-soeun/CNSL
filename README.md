## ⭐ Blockchain_이론

> [합의 알고리즘](https://github.com/Yang-soeun/CNSL/files/10706168/default.pdf)

> [이더리움](https://github.com/Yang-soeun/CNSL/files/10706133/default.pdf)

[참고문헌]
- 블록체인 구조와 이론 예제로 배우는 핀테크 핵심 기술


## ⭐ Blockchain_실습
> [블록체인 개념 & 파이썬을 이용한 블록체인 구현](https://github.com/Yang-soeun/CNSL/files/10706146/default.pdf)
> 
<details>
  
<summary> ✏ Testing Blockchain </summary>
<div markdown="1">
 
## Implementing Blockchain Using Python
- [Source_code](blockchain.py)
  
### Compotents:
- Timestamp : the time that the block was added to the blockchain
- Index : a running number starting from() indicating the block number.
- Hash of the previous block : the hash result of the previous block.
- Nonce : the number used once.
- Transaction(s) : each block will hold a variable number of transactions.
  
### Installing Flask
✔ 관리자 권한으로 실행
  
` $ pip install flask `
` $ pip install request `
  
 > Flask is a web framework that makes building web applications easy and rapid
  
## Running_terminal1
` $ python blockchain.py 5000 `
- 결과
  
![terminal1](https://user-images.githubusercontent.com/87464750/154253242-a9868d35-d29c-4b27-9d45-97cf4a6a15c2.png)

✔ 첫 번째 노드에서 실행되는 첫 번째 블록체인이 현재 실행 중인것을 볼 수 있다.

## terminal2
  
### 📑 first block
` $ curl http://localhost:5000/blockchain `
- 결과

![genesis_block](https://user-images.githubusercontent.com/87464750/154254418-83e11ca4-e3c8-435d-b885-d3f61fd16b23.png)
  
```
{
  "chain" : [{
    "hash_of_previous_block: "181cfa3e85f3c2a7aa9fb74f992d
    0d061d3e4a6d7461792413aab3f97bd3da95",
    "index" : 0,
    "nonce" : 61093,
    "timestamp" : 1644946853.955589,
    "transactions" : []
  }],
  "length" : 1
}
```
✔ 첫 번째 블록(인덱스 0)인 제니시스 블록이다.
  
### 📑 Try Mining
- Try mining a block to see how it will affect the blockchain Type the following
  
` $ curl http://localhost:5000/mine `
- 결과
  
✔ The block that is mined will now be returned:
  
![mine1](https://user-images.githubusercontent.com/87464750/154255602-91fb686f-4056-4ad9-a62e-5d0c16017955.png)

```
{
  "hash_of_previous_block": "d7a7c6ee011820a5d156c5158cb27ea48943d4817a48218829aa865bf4a21fbc",
  "index" : 1,
  "message" : "New Block Mined",
  "nonce" : 13807, 
  "transactions" : [{
    "amount" : 1,
    "recipient: "4d9de024d88d4eb7b16f4f353e5b9ddf",
    "sender" : "0"
  }]
}
```
✔  블록에 단일 트랜잭션이 포함되어 있으며 이는 채굴자에게 제공되는 보상이다.

### 📑 Obtain the blockchain from node
` $ curl http://localhost:5000/blockchain`
 
- 결과
  
✔ 이제 새로 채굴된 블록이 블록체인에 있는 것을 볼 수 있다:
  
![obtain](https://user-images.githubusercontent.com/87464750/154257790-70bc949c-cba8-49a3-8e41-f7cd1458ddc0.png)
  
```
{
  "chain" : [{
  "hash_of_previous_block: "181cfa3e85f3c2a7aa9fb74f992d
  0d061d3e4a6d7461792413aab3f97bd3da95",
  "index" : 0,
  "nonce" : 61093,
  "timestamp" : 1644946853.955589,
  "transactions" : []
}, {
  "hash_of_previous_block": "d7a7c6ee011820a5d156c5158cb27ea48943d4817a48218829aa865bf4a21fbc",
  "index" : 1,
  "message" : "New Block Mined",
  "nonce" : 13807, 
  "transactions" : [{
    "amount" : 1,
    "recipient: "4d9de024d88d4eb7b16f4f353e5b9ddf",
    "sender" : "0"
    }]
  }]
  "lenght" : 2
}
```
  
</br>
  
> Remember that the default difficulty target is set to four zero. you can change it to five zero and retest the blockchain. </br> you will realize that it now takes a longer time to mine block. since it is more difficult to find a nonce thath results in a hash beginning with five zeros.

</br>

### 📑 Add a transaction
- Let's add a transaction to a block by issuing the following command in Terminal.
  
```
$ curl -X POST -H "Content-Type: application/json" -d "{\"sender\": \"04d0988bfa799f7d7ef9ab3de97ef481\", \"recipient\": \"cd0f75d2367ad456607647edde665d6f\",\"amount\": 5}" "http://localhost:5000/transactions/new"
```
  
- 결과
  
![add](https://user-images.githubusercontent.com/87464750/154260518-56e9a9af-eb3a-474a-a71d-f42937177987.png)

✔ 성공적으로 블록이 추가되었다.
  
✔ 이제 블록을 mine 할 수 있다.
  
### 📑 Mine the block
` $ curl http://localhost:5000/mine `
- 결과

![mine2](https://user-images.githubusercontent.com/87464750/154261674-d98b2e9e-177d-4de5-814d-b13f1dbfa8be.png)
  
```
{
  "hash_of_previous_block": "7beffae74017f36dfd91d1e3a71bab570d6f10e8d97dfdae37d17d66ae7b4c32",
  "index" : 2,
  "message" : "New Block Mined",
  "nonce" : 98128, 
  "transactions" : [{
    "amount" : 5,
    "recipient: "cd0f75d2367ad456607647edde665d6f",
    "sender" : "04d0988bfa799f7d7ef9ab3de97ef481"
}, {
    "amount" : 1,
    "recipient: "4d9de024d88d4eb7b16f4f353e5b9ddf",
    "sender" : "0"
  }]
}
```
  
✔ 블록 2가 채굴되었으며 여기에는 두 개의 트랜잭션이 포함되어 있다. 하나는 수동으로 추가한 것이고 miner에 대한 보상이 있다.
 
### 📑 Add Block
- Examine the content of the blockchain by issuing this command.
  
- 결과

![last](https://user-images.githubusercontent.com/87464750/154263518-08b1befb-51d5-45d7-9cb4-8c4c42878a4a.png)

```
{
  "chain" : [{
    "hash_of_previous_block: "181cfa3e85f3c2a7aa9fb74f992d
     0d061d3e4a6d7461792413aab3f97bd3da95",
    "index" : 0,
    "nonce" : 61093,
    "timestamp" : 1644946853.955589,
    "transactions" : []
}, {
    "hash_of_previous_block": "d7a7c6ee011820a5d156c5158cb27ea48943d4817a48218829aa865bf4a21fbc",
    "index" : 1,
    "message" : "New Block Mined",
    "nonce" : 13807, 
    "transactions" : [{
      "amount" : 1,
      "recipient: "4d9de024d88d4eb7b16f4f353e5b9ddf",
      "sender" : "0"
  }]
}, {
    "hash_of_previous_block": "7beffae74017f36dfd91d1e3a71bab570d6f10e8d97dfdae37d17d66ae7b4c32",
    "index" : 2,
    "message" : "New Block Mined",
    "nonce" : 98128, 
    "transactions" : [{
      "amount" : 5,
      "recipient: "cd0f75d2367ad456607647edde665d6f",
      "sender" : "04d0988bfa799f7d7ef9ab3de97ef481"
}, {
      "amount" : 1,
      "recipient: "4d9de024d88d4eb7b16f4f353e5b9ddf",
      "sender" : "0"
    }]
  }]
  "lenght" : 3
}
```

✔ 이제 두 트랜잭션이 포함된 새로 추가된 블록이 표시된다.

 </details>
 </div>
 
<details>
  
<summary> ✏ Connecting to the Ethereum Blockchain </summary>
<div markdown="1">

- 이더리움 블록체인과 상호 작용하는데 사용할 수 있는 많은 이더리움 클라이언트가 있다.
    - Eth : A C++ Ethereum client
    - ` Geth : The official Ethereum dlient implemented using the Go programing language `
  
    - Pyethapp : A Python Ethereum client
    - Parit : An Ethereum client written using the Rust Programming language
  
- Geth를 사용.
  
### 📑 Installing Geth for Windows
  
- https://geth.ethereum.org/downloads/
    - 윈도우 버전 Geth 다운로드
  
📌 최신 버전은 --testnet이 오류가 발생함.
- https://gethstore.blob.core.windows.net/builds/geth-windows-amd64-1.9.5-a1c09b93.exe 이걸로 다운로드 받아야함.
  
### 📑 Getting Started with Geth
 - Geth를 사용하여 이더리움 블록체인에 연결
  
 ` $ geth --testnet --datadir ~/.ethereum-testnet`
  
 - --testnet: connect to the Ropsten test network.
    - Rinkeby 테스트 네트워크에 연결하고 싶다면 --rinkeby 사용.
 - --datadir: 블록체인, 키 저장소 및 기타 로컬 클라이언트 데이터를 저장하는데 사용할 로컬 저장소를 지정.
  
 - 실행결과: 네트워크의 전체 블록체인이 컴퓨터에 다운로드 되고, ~/.ethereum-testnet에 저장된다.

### 📑 Examing the Data Downloaded
![Data download](https://user-images.githubusercontent.com/87464750/155263592-20c0f9af-83ec-4964-8897-2fb7fd04317a.png)
 
 - ~/.ethereum-testnet 디렉토리에서 Geth가 만든 폴더를 볼 수 있다.
 - The geth folder contains the blockchain that you are downloading, while the keystore folder contains the account details of your local Ehtereum node.
  
### 📑 Geth javaScript Console
- To use the Geth JavaScript Console, add the following option in bold to the geth command in the Terminal.
  
` geth --testnet --datadir ~/.ethereum-testnet console 2>console.log `
  
 ![javaScript Console](https://user-images.githubusercontent.com/87464750/156876859-18f371c3-5265-4c1c-af78-7a4d1d90e40b.png)
 
- The command Prompt allows you to issue JavaScript commands
  
` personal.newAccount()`
  
![newAccount()](https://user-images.githubusercontent.com/87464750/156876920-a1add10a-f355-4581-8a5d-b49ebbfa199c.png)
  
> We will discuss more Geth commands in the next chapter.
 
 </details>
 </div>
 
 ## 📝 머신러닝
> [머신러닝.pdf](https://github.com/Yang-soeun/CNSL/files/10706068/default.pdf)

참고문헌 - 핸즈온 머신러닝 사이킷런, 케라스, 텐서플로 2를 활용한 머신러닝, 딥러닝 완벽 실무

 ## 📝 컴퓨터 보안과 암호
> [공개키-암호와-RSA](https://github.com/Yang-soeun/CNSL/files/10689194/-.-RSA.pdf)

참고문헌 - Cryptography and network security - Principles and Practice, William Stallings, Pearson.



