using Application.ViewModels.NAM.US.BKT;
using DotNetApp.ViewConfigurations.Base;

namespace DotNetApp.ViewConfigurations.NAM.US.BKT
{
    public class USBKTConfiguration : BaseAppViewConfigurations<USBKTModel>
    {
        public USBKTConfiguration(USBKTModel model) : base(model)
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