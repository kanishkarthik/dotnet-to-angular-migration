using Application.ViewModels.ASIA.India.BKT;
using DotNetApp.Core.Configuration;

namespace DotNetApp.ViewConfigurations.ASIA.India.BKT
{
    public class IndiaBKTConfiguration : PropertyConfiguration<IndiaBKTModel>
    {
        public IndiaBKTConfiguration(IndiaBKTModel model) : base(model)
        {
        }

        public override void ConfigureModel()
        {
            ConfigurePaymentMethod();
            ConfigurePaymentDetails();
            ConfigureBeneficiaryDetails();
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

            ConfigureModel(model => model.PaymentDetails.EmailAddress)
               .Name("Email Address")
               .Type("textbox");

            ConfigureModel(model => model.PaymentDetails.TranTypeCode)
                .Name("Transaction Type Code")
                .Type("lookup")
                .Required(true);

            ConfigureModel(model => model.PaymentDetails.TranTypeDesc)
                .Name("Transaction Type Description")
                .Type("textarea");
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

            ConfigureModel(model => model.BeneficiaryDetails.DestinationBranch)
                .Name("Destination Branch")
                .Type("dropdown")
                .Required(true);

            ConfigureModel(model => model.BeneficiaryDetails.AddrssLine1)
                .Name("Beneficiary Address Line 1")
                .Type("textbox");

            ConfigureModel(model => model.BeneficiaryDetails.AddrssLine2)
                .Name("Beneficiary Address Line 2")
                .Type("textbox");      
        }
    }
}