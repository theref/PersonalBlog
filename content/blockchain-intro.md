title: An Introduction to Bitcoin and Blockchain
slug: blockchain-intro
tags: blockchain, bitcoin
date: 2018-03-23
status: draft


This blog post is an accompaniment to a talk I gave at [PyDiff](http://www.pydiff.wales/).
The slides for the talk can be found [here]({filename}/pdfs/blockchain-intro.pdf) and there is recording on [YouTube](https://www.youtube.com/watch?v=-fAR9-9QzVs) as well.

## History and Background

#### Bitcoin: The first Blockchain
Bitcoin is the first Blockchain and you can't discuss one without the other.
The Blockchain is just the underlying data structure of Bitcoin.
Bitcoin couldn't exist without the Blockchain, but as soon as you have the Blockchain you inevitably also have Bitcoin.

First physical goods bought was 2 pizzas and cost 10,000 Bitcoin. Same person was also the first on the Lightning Network. Lightning Network is a 2nd layer scaling solution which I won't discuss in this talk.

First block included headline from The Times (3rd Jan) which provides insight for the motivation behind Bitcoin.

#### Definition
Quote is from Unkown because I can't remember where I heard it.
- Transparent: No information is hidden
- Public: Anyone can use it/access it
- Distributed: Running on a global network
- Append-Only: Can't be edited, only added to

#### The Ledger
Instead of using physical cash, or keeping track of everyone's individual balance, let's just record transactions. Eg Amy to Ben, Ben to Tesco etc.

| Tables        | Are           | Cool  |
|:------------- |:------------- | -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

Everyone has a copy of this ledger and all copies are identical and updated together. Now whenever someone makes a transaction it's trivial to work out their balance and see if they can spend money.

As long as we all have access to this ledger we can make financial transactions.


## More Detail
That's how I described it to my Grandparents, you probably want some more details.
Becomes a consensus problem: How do we ensure that we're all looking at the same ledger?
Let's go a bit more technical and attempt to build it as we go.

#### Hash Function
- Deterministic: Same message results in same hash
- Non-Invertible: Only way to recreate the input data is a brute force search.
- Collision Resistant: It is impossible to find 2 inputs that produce the same output.
- Avalanche Effect: a small change to a message should change the hash value so extensively that the new hash value appears uncorrelated with the old hash value

Let's look at an example:

```python
import hashlib
print(hashlib.sha256(b'hi').hexdigest())
```

Let's also write a function that can just hash a bunch inputs

```python
def quick_hash(*inputs):
    seq = (str(x) for x in inputs)
    sha = hashlib.sha256()
    sha.update(''.join(seq).encode('utf-8'))
    block_hash = sha.hexdigest()
    return block_hash

print(quick_hash([1, 2, 3], 'asdf'))
```

#### A Block
- Index: So it can be identified
- Data: Can be anything for now
- Nonce: An arbitrary number
- Hashable: Define how we Hash a Block

Create a class for a Block:
```python
class Block:
    def __init__(self, index, data):
        self.index = index
        self.data = data
        self.nonce = 0

    def __str__(self):
        return f'Block #{self.index}: {self.data} {self.hash_block()} {self.nonce}'

    def hash_block(self):
        block_hash = quick_hash(self.index, self.data, self.nonce)
        return block_hash


example_block = Block(1, 'Silly Data')
print(example_block)
```

#### Mining a Block
Also known as Proof of Work. We set a condition on the Hash of the block (start with a certain number of zeros) that can only be found by trying many different values for the nonce.

```python
class Block:
    def __init__(self, index, data):
        self.index = index
        self.data = data
        self.nonce = 0

    def __str__(self):
        return f'Block #{self.index}: {self.data} {self.hash_block()} {self.nonce}'

    def hash_block(self):
        block_hash = quick_hash(self.index, self.data, self.nonce)
        return block_hash

    def mine(self):
        block_hash = self.hash_block()
        while block_hash[:4] != '0000':
            self.nonce += 1
            block_hash = self.hash_block()
        print('Block Mined!!!')

example_block = Block(1, 'Silly Data')
print(example_block)
example_block.mine()
print(example_block, example_block.nonce)
```
If the Data in the Block changes, the Hash will no longer be valid and the block needs to be mined again.

#### A Blockchain
Link Blocks together (in a chain) by including the Hash of the previous Block.
We need to allow for the fact that the first Block (Genesis Block) won't have anything to reference.

```python
class Block:
    def __init__(self, index, data, previous_block):
        self.index = index
        self.data = data
        self.nonce = 0
        self.previous_block = previous_block

    def __str__(self):
        return f'Block #{self.index}: {self.data} {self.hash_block()} {self.nonce}'

    def hash_block(self):
        if self.previous_block == 'Genesis':
            previous_hash = 'Genesis_Hash'
        else:
            previous_hash = self.previous_block.hash_block()
        block_hash = quick_hash(self.index, self.data, self.nonce, previous_hash)
        return block_hash

    def mine(self):
        block_hash = self.hash_block()
        while block_hash[:4] != '0000':
            self.nonce += 1
            block_hash = self.hash_block()
        print('Block Mined!!!')

genesis_block = Block(0, 'Our First Block', 'Genesis')
print(genesis_block)
genesis_block.mine()
print(genesis_block)

example_block = Block(1, 'Silly Data', genesis_block)
print(example_block)
example_block.mine()
print(example_block)

genesis_block.data = 'Genesis Block'
print(genesis_block)
print(example_block)

genesis_block.mine()
print(genesis_block)
print(example_block)

example_block.mine()
print(example_block)
```
If the Previous Hash or the Data changes, the Block needs to be mined again.
If we change something in a previous Block (regardless of how far in the past) the current Block will be invalid.

Lets make a longer Blockchain:

```python
blockchain = [genesis_block]
for i in range(1, 8):
    new_block = Block(index=i,
                      data='some data here',
                      previous_block=blockchain[-1])
    new_block.mine()
    blockchain.append(new_block)
    print(new_block)
```
We can see that some of them took longer than others.
What happens if a malicious attacker tries to edit some of the data?

```python
blockchain[2].data = 'Malicious Attack'
for block in blockchain:
    print(block)

for block in blockchain[2:]:
    block.mine()
    print(block)
```
They have to redo all of the computations for the previous blocks. Hence the phrase 'Proof of Work'. It takes CPU power to mine a Block so that it's valid and can be included in the Blockchain.


## Even More Detail
I've explained the Data structure but I said it was a public, distributed network

#### The Blockchain Process
Going to link this to Bitcoin because it's a great example. Now need to imagine that this process is running globally on many computers.

- A user creates an addition to the ledger, for Bitcoin this would be a transaction
- Everyone in the Network can see that the user is attempting to make this transaction
- For Bitcoin, they package several transactions into a Block and race to find the appropriate Nonce
- When a Node finds an appropriate Nonce, the Block is added to the Blockchain and broadcast to the Network
- The process repeats with Nodes now attempting to find the next Block

Nodes in the network use the longest Blockchain available. As soon as they receive a new, valid block they move on and start building the next one. In the (very rare) event that two Blocks are created simultaneously, the network forks. Some nodes follow one branch, some follow the other. At some point (the next block) one fork will become longer and all nodes use that one.


#### A Malicious Node
Attack goes back and edits B3 and computes new Nonce. Attackers chain is now 2 blocks behind the main chain and so is not recognised by the rest of the network (use longest chain).
Has to redo PoW for B4 and B5 in order for their Blockchain to be used by rest of network.

However, in that time, 'good' nodes will continue to add Blocks to the original chain. The attacker will not be able to catch up and the network will never include the malicious Block.


## Tell Me More About Bitcoin
We've covered the Blockchain. We now have a process where we can be sure that we're all looking at the same ledger (we've acheived consensus). Been quite vague about several things...eg the nature of the data (that was to keep things very general), could be used for supply chain, medical records etc.

This isn't enough for a digital currency like Bitcoin.

#### Unanswered Issues
- Incentive for Good nodes, owning and running a pc costs money...why would I bother?
- At no point where any Bitcoins actually created, we've only covered how to transfer them
- Proof of Ownership, what stops someone else creating a transaction that spends my Bitcoins?

#### Coinbase Transaction
The first two issues are solved together. Every Block includes a transaction that has no sender, only a receiver. This is called a coinbase transaction. The value of the transaction is called a Block Reward and the recipient is the Node that successfully mines the Block (finds the correct Nonce).

The Block Reward (currently 12.5 B) decreases over time to ensure that there is a finite supply of Bitcoin (21 million). Currently mined 17 million.

We've now incentives good nodes and we call them miners and we have a way to gradually introduce new Bitcoins to the network in a predictable way.

Lets quickly put all this together using a tool that someone else made that was what I had intended to make just much better.

#### Public/Private Key Pairs
Very common throughout cyber-security.
Instead of using names, we generate a public/private key pair, and the public key becomes our Bitcoin address.

When a transaction is created, the sender creates the signature of the transaction, using their private key. Thus anyone can easily verify that the transaction was created by the sender **only**.


## Tell Me More


#### Further Reading (Bitcoin)
- Environmental Impact: lots of headlines in the media about Bitcoin using more electricity than Denmark. Wildly varying estimates. Less than USA uses on Christmas lights.
- Merkle Trees: How do we actually hash transaction such that it's efficient and easy to verify that a transaction exists.
- Segwit and Lightning: Both have been recently activated. Segwit makes blocks more efficient (therefore lower fees) and is a pre-requisite for Lightning. Lightning is a 2nd layer solution that allows for off chain, instant, near fee-less transactions.


#### Further Reading (future of Blockchain)
- Proof of Stake; alternative to PoW. Miners selected based on wealth.
- Smart Contracts; code is stored on Blockchain and executed by the network
- DAG Currencies; replace linear Blockchain with Directed Acyclic Graphs
- Hashgraphs; DAG on steroids, uses a gossip protocol
