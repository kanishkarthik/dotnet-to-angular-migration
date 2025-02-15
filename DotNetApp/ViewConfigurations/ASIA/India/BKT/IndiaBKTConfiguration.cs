using Application.ViewModels.ASIA.India.BKT;
using DotNetApp.ViewConfigurations.Base;

namespace DotNetApp.ViewConfigurations.ASIA.India.BKT
{
    public class IndiaBKTConfiguration : BaseAppViewConfigurations<IndiaBKTModel>
    {
        public IndiaBKTConfiguration(IndiaBKTModel model) : base(model)
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

            //Order 4
            ConfigureOrderingPartyDetails();
        }

        public void ConfigurePaymentDetails()
        {
            ConfigureModel(model => model.PaymentDetails.TranRefNo)
                .Name("Transaction Reference Number")
                .Type("textbox")
                .Required(true)
                .MaxLength(10)
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
               .Type("textbox")
               .Pattern("[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+");

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
        public void ConfigureOrderingPartyDetails()
        {
            ConfigureModel(model => model.OrderingPartyDetails.Name)
                 .Name("Ordering Party Name")
                 .Type("textbox")
                 .MaxLength(50);

            ConfigureModel(model => model.OrderingPartyDetails.Address)
                .Name("Ordering Party Address")
                .Type("textarea");
        }
    }
}