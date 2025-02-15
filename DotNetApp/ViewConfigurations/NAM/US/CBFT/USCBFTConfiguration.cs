using Application.ViewModels.NAM.US.CBFT;
using DotNetApp.Core.Configuration;

namespace DotNetApp.ViewConfigurations.NAM.US.CBFT
{
    public class USCBFTConfiguration : PropertyConfiguration<USCBFTModel>
    {
        public USCBFTConfiguration(USCBFTModel model) : base(model)
        {
        }

        public override void ConfigureModel()
        {
            ConfigurePaymentMethod();
            ConfigurePaymentDetails();
            ConfigureBeneficiaryDetails();
        }

        private void ConfigurePaymentMethod()
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
        }

        private void ConfigurePaymentDetails()
        {
            ConfigureModel(model => model.PaymentDetails.TransactionReferenceNumber)
                .Name("Transaction Reference")
                .Type("textbox")
                .Required(true)
                .Pattern("[A-Z0-9]+")
                .MaxLength(16);

            ConfigureModel(model => model.PaymentDetails.ValueDate)
                .Name("Value Date")
                .Type("date")
                .Required(true);

            ConfigureModel(model => model.PaymentDetails.IsUrgentPayment)
                .Name("Urgent Payment")
                .Type("checkbox");

            ConfigureModel(model => model.PaymentDetails.PaymentPurpose)
                .Name("Payment Purpose")
                .Type("dropdown")
                .Required(true);

            ConfigureModel(model => model.PaymentDetails.RemittanceInformation)
                .Name("Remittance Information")
                .Type("textarea")
                .MaxLength(140);

            ConfigureModel(model => model.PaymentDetails.HasIntermediaryBank)
                .Name("Has Intermediary Bank")
                .Type("checkbox");

            ConfigureModel(model => model.PaymentDetails.IntermediaryBankCode)
                .Name("Intermediary Bank Code")
                .Type("textbox");
                //.DependsOn("HasIntermediaryBank");
        }

        private void ConfigureBeneficiaryDetails()
        {
            ConfigureModel(model => model.BeneficiaryDetails.BeneficiaryName)
                .Name("Beneficiary Name")
                .Type("textbox")
                .Required(true)
                .MaxLength(35);

            ConfigureModel(model => model.BeneficiaryDetails.AccountNumber)
                .Name("Account Number")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.BankName)
                .Name("Bank Name")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.RoutingNumber)
                .Name("ACH Routing Number")
                .Type("textbox")
                .Required(true)
                .Pattern("[0-9]{9}");

            ConfigureModel(model => model.BeneficiaryDetails.BankAddress)
                .Name("Bank Address")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.StateCode)
                .Name("State")
                .Type("dropdown")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.ZipCode)
                .Name("ZIP Code")
                .Type("textbox")
                .Required(true)
                .Pattern("[0-9]{5}(-[0-9]{4})?");
        }
    }
}
