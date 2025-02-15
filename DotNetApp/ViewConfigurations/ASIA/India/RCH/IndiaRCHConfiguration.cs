using Application.ViewModels.ASIA.India.RCH;
using DotNetApp.ViewConfigurations.Base;

namespace DotNetApp.ViewConfigurations.ASIA.India.RCH
{
    public class IndiaRCHConfiguration : BaseAppViewConfigurations<IndiaRCHModel>
    {
        public IndiaRCHConfiguration(IndiaRCHModel model) : base(model)
        {
        }

        public override void ConfigureModel()
        {
            //Order 1
            ConfigurePaymentMethod();
            //Order 2
            ConfigurePaymentDetails();
            //Order 3
            ConfigureChequeDetails();
        }

        private void ConfigurePaymentDetails()
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

        private void ConfigureChequeDetails()
        {
            ConfigureModel(model => model.ChequeDetails.ChequeNumber)
                .Name("Cheque Number")
                .Type("textbox")
                .Required(true)
                .Pattern("^[0-9]{6}$");

            ConfigureModel(model => model.ChequeDetails.PayeeName)
                .Name("Payee Name")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.ChequeDetails.ChequeDate)
                .Name("Cheque Date")
                .Type("date")
                .Required(true);

            ConfigureModel(model => model.ChequeDetails.ChequeType)
                .Name("Cheque Type")
                .Type("dropdown")
                .Required(true);

            ConfigureModel(model => model.ChequeDetails.DeliveryMethod)
                .Name("Delivery Method")
                .Type("dropdown")
                .Required(true);

            ConfigureModel(model => model.ChequeDetails.DeliveryAddress)
                .Name("Delivery Address")
                .Type("textarea")
                .Required(true);

            ConfigureModel(model => model.ChequeDetails.ContactNumber)
                .Name("Contact Number")
                .Type("textbox")
                .Required(true)
                .Pattern(@"^\+?[0-9]{10,12}$");

            ConfigureModel(model => model.ChequeDetails.SpecialInstructions)
                .Name("Special Instructions")
                .Type("textarea");
        }
    }
}
