using Application.ViewModels.ASIA.India.CBFT;
using DotNetApp.ViewConfigurations.Base;

namespace DotNetApp.ViewConfigurations.ASIA.India.CBFT
{
    public class IndiaCBFTConfiguration : BaseAppViewConfigurations<IndiaCBFTModel>
    {
        public IndiaCBFTConfiguration(IndiaCBFTModel model) : base(model)
        {
        }

        public override void ConfigureModel()
        {
            //Order 1
            ConfigurePaymentMethod();

            //Order 2
            ConfigurePaymentDetails();

            //Order 3
            ConfigureBeneficiaryDetails();
        }

        public new void ConfigurePaymentMethod()
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
                .MaxLength(3)
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
                .Pattern("[a-zA-Z0-9]+")
                .MaxLength(20);

            ConfigureModel(model => model.PaymentDetails.ValueDate)
                .Name("Value Date")
                .Type("date")
                .Required(true);

            ConfigureModel(model => model.PaymentDetails.isUrgent)
                .Name("Urgent Payment")
                .Type("checkbox");

            ConfigureModel(model => model.PaymentDetails.PurposeCode)
                .Name("Purpose Code")
                .Type("lookup")
                .Required(true);

            ConfigureModel(model => model.PaymentDetails.PurposeDescription)
                .Name("Purpose Description")
                .Type("textarea");

            ConfigureModel(model => model.PaymentDetails.RemittanceInfo)
                .Name("Remittance Information")
                .Type("textarea")
                .Required(true);
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

            ConfigureModel(model => model.BeneficiaryDetails.BeneBank)
                .Name("Beneficiary Bank")
                .Type("lookup")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.BeneBankCode)
                .Name("Beneficiary Bank Code")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.BeneCountry)
                .Name("Beneficiary Country")
                .Type("dropdown")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.AddrssLine1)
                .Name("Beneficiary Address Line 1")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.AddrssLine2)
                .Name("Beneficiary Address Line 2")
                .Type("textbox");
        }
    }
}
