using Application.ViewModels.NAM.US.BKT;
using DotNetApp.Core.Configuration;
using System;

namespace DotNetApp.ViewConfigurations.NAM.US.BKT
{
    public class USBKTConfiguration : PropertyConfiguration<USBKTModel>
    {
        public USBKTConfiguration(USBKTModel model) : base(model)
        {
        }

        public override void ConfigureModel()
        {
            ConfigurePaymentMethod();
            ConfigurePaymentDetails();
            ConfigureBeneficiaryDetails();
            ConfigureOrderingPartyDetails();
        }

        
        public void ConfigurePaymentMethod()
        {
            ConfigureModel(model => model.PaymentMethod.AccountNumber)
                .Name("Account Number")
                .Type("label");

            ConfigureModel(model => model.PaymentMethod.PaymentCurrency)
                .Name("Payment Currency")
                .Type("label");

            ConfigureModel(model => model.PaymentMethod.Amount)
                .Name("Payment Amount")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.PaymentMethod.AccountName)
                .Name("Account Name")
                .Type("label");

            ConfigureModel(model => model.PaymentMethod.PaymentMethod)
                .Name("Payment Method")
                .Type("label");
        }

        public void ConfigurePaymentDetails()
        {
            ConfigureModel(model => model.PaymentDetails.TranRefNo)
                .Name("Transaction Reference Number")
                .Type("textbox")
                .Required(true)
                .Pattern("[a-zA-Z0-9]+");

            ConfigureModel(model => model.PaymentDetails.ValueDate)
                .Name("Value Date")
                .Type("date")
                .Required(true);

            ConfigureModel(model => model.PaymentDetails.isConfidential)
                .Name("Confidential")
                .Type("checkbox");
        }

        public void ConfigureBeneficiaryDetails()
        {
            ConfigureModel(model => model.BeneficiaryDetails.BeneName)
                .Name("Beneficiary Name")
                .Type("lookup")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.BeneAcctNo)
                .Name("Beneficiary Account Number")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.AddrssLine1)
                .Name("Beneficiary Address Line 1")
                .Type("textbox");

            ConfigureModel(model => model.BeneficiaryDetails.AddrssLine2)
                .Name("Beneficiary Address Line 2")
                .Type("textbox");      
        }

        private void ConfigureOrderingPartyDetails()
        {
            ConfigureModel(model => model.OrderingPartyDetails.Name)
              .Name("Ordering Party Name")
              .Type("textbox")
              .Pattern("[a-zA-Z0-9]+");
        }
    }
}