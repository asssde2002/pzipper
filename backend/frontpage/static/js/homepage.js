async function startHardhatServer() {
    try {
        let response = await fetch('/blockchain/ping-hardhat/');
        let data = await response.json();
        if (!data["SUCCESS"]) throw new Error(`HTTP error! error: ${data["ERR_MSG"]}`);
        document.getElementById("hardhat-response").innerText = data["PAYLOAD"] || "Hardhat Server is ready!";
    } catch (error) {
        console.error("Error pinging Hardhat:", error);
        document.getElementById("hardhat-response").innerText = "Failed to reach Hardhat.";
    }
}

async function increaseCount() {
    try {
        let response = await fetch('blockchain/smartcontract-counter/increase-count/', {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        let data = await response.json();
        if (!data["SUCCESS"]) throw new Error(`HTTP error! error: ${data["ERR_MSG"]}`);
        alert("Count increased successfully!");
    } catch (error) {
        alert("Fail to increase count.");
    }
}

async function getCount() {
    try {
        let response = await fetch('blockchain/smartcontract-counter/get-count/', {
            method: "GET",
        });
        let data = await response.json();
        if (!data["SUCCESS"]) throw new Error(`HTTP error! error: ${data["ERR_MSG"]}`);
        alert(`Current count: ${data["PAYLOAD"]["current_count"]}`);
    } catch (error) {
        alert("Fail to get count.");
    }
}

async function uploadSmartContract() {
    const fileInput = document.getElementById("contractFile");
    const file = fileInput.files[0];

    let formData = new FormData();
    formData.append("data", file);

    try {
        let response = await fetch('/blockchain/smartcontract/', {
            method: "POST",
            body: formData
        });

        let data = await response.json();
        if (!data["SUCCESS"]) throw new Error(`HTTP error! error: ${data["ERR_MSG"]}`);
        if (response.ok) {
            alert("Contract uploaded successfully!");
            getSmartContract();
        } else {
            alert(`Upload failed: ${data.error || "Unknown error"}`);
        }
    } catch (error) {
        console.error("Error uploading contract:", error);
        alert("Upload failed.");
    }
}

async function deploySmartContract(contractID, buttonElement) {
    try {
        buttonElement.disabled = true;
        buttonElement.innerText = "Deploying...";

        let response = await fetch('/blockchain/deployment/', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ contract_id: contractID })
        });

        let data = await response.json();
        if (!data["SUCCESS"]) throw new Error(`HTTP error! error: ${data["ERR_MSG"]}`);
        if (response.ok) {
            alert(`Contract deployed successfully!`);
            getContractDeployment(contractID); 
        } else {
            alert(`Deployment failed: ${data.error || "Unknown error"}`);
        }
    } catch (error) {
        console.error("Error deploying contract:", error);
        alert("Deployment failed.");
    } finally {
        buttonElement.disabled = false;
        buttonElement.innerText = "Deploy";
    }
}


async function getSmartContract() {
    try {
        let response = await fetch('/blockchain/smartcontract/', { method: "GET" });
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        
        let data = await response.json();
        if (!data["SUCCESS"]) throw new Error(`HTTP error! error: ${data["ERR_MSG"]}`);
        contracts = data["PAYLOAD"]
        console.log("Contracts Fetched:", contracts);
        renderContracts(contracts);
    } catch (error) {
        console.error("Error fetching contracts:", error);
    }
}


async function getContractDeployment(contractID) {
    try {
        const response = await fetch(`/blockchain/deployment/?contract_id=${contractID}`);
        const data = await response.json();
        if (!data["SUCCESS"]) throw new Error(`HTTP error! error: ${data["ERR_MSG"]}`);
        let deployment_data = data["PAYLOAD"]

        let deploymentTable = document.getElementById(`deployment-${contractID}`);
        deploymentTable.innerHTML = ""
        if (deployment_data && deployment_data.length > 0) {
            deployment_data.forEach(dep => {
                let row = document.createElement("tr");
                row.innerHTML = `
                    <td>${dep.address || "Not Deployed"}</td>
                    <td>${dep.deployed_at || "N/A"}</td>
                `;
                deploymentTable.appendChild(row);
            });
        } else {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td colspan="2">No deployments available</td>
            `;
            deploymentTable.appendChild(row);
        }
    } catch (error) {
        console.error("Error fetching deployments:", error);
    }
}

function renderContracts(contracts) {
    let container = document.getElementById("contractList");
    container.innerHTML = "";

    contracts.forEach(contract => {
        let contractBlock = document.createElement("div");
        contractBlock.className = "contract-container";
        contractBlock.setAttribute("data-contract-id", contract.id);
        contractBlock.innerHTML = `
            <div class="contract-header">
                <h2>${contract.contract_name}</h2>
                <button class="contract-button" onclick="deploySmartContract(${contract.id}, this)">Deploy</button>
                ${contract.contract_name === "Counter" ? `
                    <button class="contract-button" onclick="increaseCount()">Increase Count</button>
                    <button class="contract-button" onclick="getCount()">Get Count</button>
                ` : ''}
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Address</th>
                        <th>Deployed At</th>
                    </tr>
                </thead>
                <tbody id="deployment-${contract.id}">
                    <!-- Deployment rows will be inserted here -->
                </tbody>
            </table>
        `;
        container.appendChild(contractBlock);
        getContractDeployment(contract.id)
    });
}

getSmartContract()