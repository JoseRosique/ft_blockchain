<a href="https://github.com/JaeSeoKim/badge42"><img src="https://badge42.vercel.app/api/v2/cl4qxms4g001609l49j835g66/project/3079334" alt="joslopez's 42 ft_blockchain Score" /></a>
<h2>General Instructions</h2> <p>For this project you can use any programming language. You can use [cryptographic libraries] like openssl or hashlib for generating hashes, but the [blockchain structure] must be implemented by you. In the same way, a [web framework] like NestJS or Flask can be used for the server implementation.</p> <pre> <span style="color: #4e9a06;">block</span> <span style="color: #75507b;">=</span> { <span style="color: #4e9a06;">'index'</span><span style="color: #75507b;">:</span> <span style="color: #3465a4;">4</span><span style="color: #75507b;">,</span> <span style="color: #4e9a06;">'timestamp'</span><span style="color: #75507b;">:</span> <span style="color: #3465a4;">1644045050.00042</span><span style="color: #75507b;">,</span> <span style="color: #4e9a06;">'transactions'</span><span style="color: #75507b;">:</span> [ { <span style="color: #4e9a06;">'sender'</span><span style="color: #75507b;">:</span> <span style="color: #cc0000;">'4c6e7e2a9f2f7f7ff8e7d3d6c8b7c6e8e23a7'</span><span style="color: #75507b;">,</span> <span style="color: #4e9a06;">'recipient'</span><span style="color: #75507b;">:</span> <span style="color: #cc0000;">'b3c6e7e2a9f2f7f7ff8e7d3d6c8b7c6e8e23a7'</span><span style="color: #75507b;">,</span> <span style="color: #4e9a06;">'amount'</span><span style="color: #75507b;">:</span> <span style="color: #3465a4;">42</span><span style="color: #75507b;">,</span> } ]<span style="color: #75507b;">,</span> <span style="color: #4e9a06;">'proof'</span><span style="color: #75507b;">:</span> <span style="color: #3465a4;">324984774000</span><span style="color: #75507b;">,</span> <span style="color: #4e9a06;">'previous_hash'</span><span style="color: #75507b;">:</span> <span style="color: #cc0000;">'084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc0'</span><span style="color: #75507b;">,</span> } </pre> <p>Example of a block. The hash of the above block has been generated using the [SHA256 algorithm].</p>  <h2>Mandatory Part</h2> <p>The workflow is to add different transactions to the current block and mine the block so that the chain is added.</p> <p>The proof-of-work algorithm should be simple, for example, finding the number that, concatenated with the previous proof-of-work, matches the result of the SHA-256 hash ending in 4242. The chain of blocks will not be persistent, it will be stored in the memory of the server but the server will not be connected to any specific database software. When developing mining, three things must be done:</p> <ul> <li>Calculate proof of work</li> <li>Reward miners (one transaction)</li> <li>Creation of the new block and add it to the chain</li> </ul> <p>Once the blockchain is created, you can interact with it through different [HTTP requests] on a text-based API:</p> <ul> <li>[POST] /transactions/new : Post a new transaction to add to the next block.</li> <li>[GET] /mine : Execute the [proof of work] and create a new block.</li> <li>[GET] /chain : Returns information about the full blockchain (blocks, transactions, etc).</li> </ul>  <h2>Bonus Part</h2> <p>The evaluation of the bonuses will be done IF AND ONLY IF the mandatory part is PERFECT. Otherwise, the bonuses will be totally IGNORED.</p> <p>You can enhance your project with the following features:</p> <ul> <li>Difficulty of the [dynamic PoW algorithm], ascending depending on the number of mined blocks or the elapsed time.</li> <li>Implementation of communication with other network nodes through a [decentralized network] and a [consensus algorithm] to verify the correct chain.</li> <li>[Proof of Stake] in addition to Proof of Work, as an alternative, eco-friendly consensus algorithm.</li> <li>Everything that comes to your mind... you will be able to justify everything during the defense.</li> </ul>
