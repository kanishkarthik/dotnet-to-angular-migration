window.onload = function () {
    initializePayments();
}
function openDialog(referenceNumber) {
    const dialog = document.getElementById('success-dialog');
    const refNumberSpan = document.getElementById('reference-number');
    refNumberSpan.textContent = referenceNumber; // Set the reference number dynamically
    dialog.classList.remove('hidden');
}

function closeDialog() {
    const dialog = document.getElementById('success-dialog');
    dialog.classList.add('hidden');
    window.location = "/";
}


var initializePayments = function () {

    const headerPaymentDetails = sessionStorage.getItem("paymentHeaderDetails");

    const paymentDetails = JSON.parse(headerPaymentDetails);
    console.log(paymentDetails);
    document.getElementById("PaymentMethod.AccountNumber").innerText = paymentDetails.account.number;
    document.getElementById("PaymentMethod.AccountName").innerText = paymentDetails.account.name;
    document.getElementById("PaymentMethod.PaymentMethod").innerText = paymentDetails.payment.methodDesc;
    document.getElementById("PaymentMethod.PaymentCurrency").innerText = paymentDetails.account.currency;


    document.getElementsByClassName("primary")[0].addEventListener("click", function () {
        const referenceNumber = document.getElementById("PaymentDetails.TranRefNo").value;
        openDialog(referenceNumber);
    });

    document.getElementsByClassName("secondary")[0].addEventListener("click", function () {

        window.location = "/";
    });
    const popupDiv = document.createElement('div');
    popupDiv.innerHTML = `<div id="success-dialog" class="success-dialog hidden">
    <div class="dialog-content">
        <h3>Payment Submitted Successfully</h3>
        <p>Your payment has been successfully initiated. Reference Number: <span id="reference-number">12345678</span></p>
        <button class="primary" onclick="closeDialog()">OK</button>
    </div>
</div>`;
    document.body.appendChild(popupDiv);
}

const lookupOptions = [
        {
            name: 'PaymentDetails_TranTypeCode',
            label: 'Select Transaction Type Code',
            headers: ['Account Number', 'Account Name', 'Branch Name'],
            optionsName: ['number', 'name', 'branchName'],
            optionsValue: [
                { number: '14447026', name: 'Account 1', branchName: 'CITIBANK NA LONDON', branchCode: 101, countryCode: 'IN', balance: '20.00 INR' },
            ]
        }, {
        name: 'BeneficiaryDetails_BeneName',
            label: 'Select Beneficiary',
            headers: ['Currency Code', 'Currency Name'],
            optionsName: ['code', 'name'],
            optionsValue: [
                { code: 'INR', name: 'INDIAN RUPEE' }
            ]
        }
];

function openPopup(popupId) {
    document.querySelector(`.popup.${popupId}`).style.display = 'block';
    document.querySelector('.overlay').style.display = 'block';
}

function closePopup(popupId) {
    document.querySelector(`.popup.${popupId}`).style.display = 'none';
    document.querySelector('.overlay').style.display = 'none';
}

function createPopup(lookup, id, name) {
    const headers = ['name', 'description'];
    const optionsValue = [
        { name: 'Item 1', description: 'Item 1' },
        { name: 'Item 2', description: 'Item 2' },
        { name: 'Item 3', description: 'Item 3' },
        { name: 'Item 4', description: 'Item 4' },
        { name: 'Item 5', description: 'Item 5' },
        { name: 'Item 6', description: 'Item 6' }
    ],
        optionsName = ['name', 'description']
        ;
    // Create the main popup container
    const popupDiv = document.createElement('div');
    popupDiv.className = `popup ${id.replace('.', '_')}`;
    popupDiv.innerHTML = `
        <div class="popup-header">${name.replace('*', '')} Lookup</div>
        <table>
            <thead>
                <tr>
                    ${headers.map(header => `<th>${header}</th>`).join('')}
                    <th></th>
                </tr>
            </thead>
            <tbody>
                ${optionsValue.map((option) => `
                    <tr>
                         ${optionsName.map((name) => `
                         <td>${option[name]}</td>
                         `).join('')}
                        <td>
                            <button onclick="selectOption('${id}', '${encodeURIComponent(JSON.stringify(option))}')">Select</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
        
    `;

    // Append the popup to the body
    document.body.appendChild(popupDiv);
}

// Function to dynamically add all popups
function initializePopups(lookupOptions) {
    var lookups = document.querySelectorAll(".lookup-item");
    lookups.forEach(lookup => {
        let id = lookup.querySelector("input[type=text]").id,
            name = lookup.querySelector("label").innerText;
        createPopup(lookup, id, name);
    });
    //lookupOptions.forEach(option => createPopup(option));
}

// Function to handle option selection
function selectOption(id, option) {
    option = JSON.parse(decodeURIComponent(option));
    console.log(`Selected from ${name}:`, option);
    // Handle specific logic for selection (e.g., updating input fields)
        //paymentHeaderDetails.account = option;
    document.getElementById(id).value = option.name;
    closePopup(id.replace(".", "_"));
}

// Initialize all popups
initializePopups(lookupOptions);

function initializeDropdown() {
    const dropdowns = document.querySelectorAll("select");
    dropdowns.forEach(dropdown => {
        populateDropdown(dropdown);

    });
}
// Add options dynamically to the dropdown
function populateDropdown(dropdown) {
    const options = [
        { value: 'option1', label: 'Option 1' },
        { value: 'option2', label: 'Option 2' },
        { value: 'option3', label: 'Option 3' }
    ]
    let label = dropdown.previousElementSibling.innerText.replace("*", "");
    let newOption = document.createElement('option');
    newOption.value = "";
    newOption.textContent = "--Select " + label + " --";
    newOption.setAttribute("disabled", "disabled");
    newOption.setAttribute("selected", "selected");
    dropdown.appendChild(newOption);
    options.forEach(option => {
        newOption = document.createElement('option');
        newOption.value = option.value;
        newOption.textContent = option.label;
        dropdown.appendChild(newOption);
    });
}

// Adding a new option dynamically via button click
function addOption() {
    const newOption = document.createElement('option');
    newOption.value = 'newOption';
    newOption.textContent = 'New Option';
    dropdown.appendChild(newOption);
}

initializeDropdown();