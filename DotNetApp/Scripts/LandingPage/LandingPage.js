function openPopup(popupId) {
    document.querySelector(`.popup.${popupId}`).style.display = 'block';
    document.querySelector('.overlay').style.display = 'block';
}

function closePopup(popupId) {
    document.querySelector(`.popup.${popupId}`).style.display = 'none';
    document.querySelector('.overlay').style.display = 'none';
}

const paymentHeaderDetails = {
    account: {},
    payment: {},
},
    lookupOptions = [
        {
            name: 'AccountNumber',
            label: 'Select Account Number',
            headers: ['Account Number', 'Account Name', 'Currency', 'Country Code'],
            optionsName: ['number', 'name', 'currency', 'countryCode'],
            optionsValue: [
                { number: '14447026', name: 'Account 1', currency: 'INR', countryCode: 'IN' },
            ]
        }
    ],
    paymentMethods = [
        {
            code: 'BKT',
            name: 'Book Transfer',
            types: []
        },
        {
            code: 'RCH',
            name: 'Cheque',
            types: []
        },
        {
            code: 'DFT',
            name: 'Domestic Funds Transfer',
            types: []
        },
        {
            code: 'EFT',
            name: 'Cross Border Funds Transfer',
            types: []
        }
    ];

function createPopup({ name, label, headers, optionsName, optionsValue }) {
    // Create the main popup container
    const popupDiv = document.createElement('div');
    popupDiv.className = `popup ${name}`;
    popupDiv.innerHTML = `
        <div class="popup-header">${label}</div>
        <table>
            <thead>
                <tr>
                    ${headers.map(header => `<th>${header}</th>`).join('')}
                    <th>Select</th>
                </tr>
            </thead>
            <tbody>
                ${optionsValue.map((option) => `
                    <tr>
                         ${optionsName.map((name) => `
                         <td>${option[name]}</td>
                         `).join('')}
                        <td>
                            <button onclick="selectOption('${name}', '${encodeURIComponent(JSON.stringify(option))}')">Select</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
        <button onclick="closePopup('${name}')">Close</button>
    `;

    // Append the popup to the body
    document.body.appendChild(popupDiv);
}

// Function to dynamically add all popups
function initializePopups(lookupOptions) {
    lookupOptions.forEach(option => createPopup(option));
}

// Function to handle option selection
function selectOption(name, option) {
    option = JSON.parse(decodeURIComponent(option));
    console.log(`Selected from ${name}:`, option);
    // Handle specific logic for selection (e.g., updating input fields)
    if (name === 'AccountNumber') {
        paymentHeaderDetails.account = option;
        document.getElementById('AccountNumber').value = option.number;
        document.querySelector('.info.AccountNumber').innerHTML = `Account Name: ${option.name}`;
    }
    closePopup(name);
}

// Initialize all popups
initializePopups(lookupOptions);

// Additional functionality for Payment Methods

function initializePaymentMethods(paymentMethods) {
    const paymentMethod = document.getElementById('PaymentMethod');
    var option = document.createElement('option');
    option.text = 'Select Payment Method';
    option.value = '';
    paymentMethod.add(option);
    paymentMethods.forEach(method => {
        option = document.createElement('option');
        option.text = method.name;
        option.value = method.code;
        paymentMethod.add(option);
    });
    paymentMethod.addEventListener('change', function () {
        const selectedPaymentMethod = paymentMethod.value;
        paymentHeaderDetails.payment.methodCode = selectedPaymentMethod;
        paymentHeaderDetails.payment.methodDesc = paymentMethods.find(item => item.code == selectedPaymentMethod).name;
    });

}

initializePaymentMethods(paymentMethods);

window.onload = function () {
    const routes = {
        'in_bkt': 'indiabkt'
    }
    document.getElementById('continue').addEventListener('click', function () {
        const paymentMethod = document.getElementById('PaymentMethod').value;
        if (paymentMethod) {
            //alert(JSON.stringify(paymentHeaderDetails));
            sessionStorage.setItem("paymentHeaderDetails", JSON.stringify(paymentHeaderDetails));
            window.location = routes[paymentHeaderDetails.account.countryCode.toLowerCase() + "_" + paymentHeaderDetails.payment.methodCode.toLowerCase()];
        }
    });
};




