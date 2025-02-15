using Application.ViewModels.ASIA.India.DFT;
using DotNetApp.ViewConfigurations.Base;

namespace DotNetApp.ViewConfigurations.ASIA.India.DFT
{
    public class IndiaDFTConfiguration : BaseAppViewConfigurations<IndiaDFTModel>
    {
        public IndiaDFTConfiguration(IndiaDFTModel model) : base(model)
        {
        }

        public override void ConfigureModel()
        {
            ConfigurePaymentMethod();
            ConfigureTransferDetails();
            ConfigureBeneficiary();
            ConfigureAdditionalOptions();
        }

        private void ConfigureTransferDetails()
        {
            ConfigureModel(model => model.TransferDetails.TransferReferenceNumber)
                .Name("Transfer Reference Number")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.TransferDetails.TransferDate)
                .Name("Transfer Date")
                .Type("date")
                .Required(true);

            ConfigureModel(model => model.TransferDetails.TransferType)
                .Name("Transfer Date")
                .Type("dropdown")
                .Required(true);

            ConfigureModel(model => model.TransferDetails.PaymentPurpose)
                .Name("Payment Purpose")
                .Type("dropdown")
                .Required(true);

            ConfigureModel(model => model.TransferDetails.Remarks)
                .Name("Remarks")
                .Type("textarea")
                .MaxLength(100);
        }

        private void ConfigureBeneficiary()
        {
            ConfigureModel(model => model.Beneficiary.BeneficiaryName)
                .Name("Beneficiary Name")
                .Type("textbox")
                .Required(true)
                .MaxLength(50);

            ConfigureModel(model => model.Beneficiary.BeneficiaryAccountNumber)
                .Name("Beneficiary Account Number")
                .Type("textbox")
                .Required(true)
                .Pattern(@"^\d{8,20}$");

            ConfigureModel(model => model.Beneficiary.BeneficiaryBankName)
                .Name("Beneficiary Bank")
                .Type("dropdown")
                .Required(true);

            ConfigureModel(model => model.Beneficiary.BeneficiaryIFSCCode)
                .Name("IFSC Code")
                .Type("textbox")
                .Required(true)
                .Pattern(@"^[A-Z]{4}0[A-Z0-9]{6}$");

            ConfigureModel(model => model.Beneficiary.BeneficiaryBankBranch)
                .Name("Bank Branch")
                .Type("textbox");

            ConfigureModel(model => model.Beneficiary.BeneficiaryAddress)
                .Name("Beneficiary Address")
                .Type("textarea")
                .MaxLength(200);
        }

        private void ConfigureAdditionalOptions()
        {
            ConfigureModel(model => model.AdditionalOptions.IsUrgentPayment)
                .Name("Urgent Payment")
                .Type("checkbox");

            ConfigureModel(model => model.AdditionalOptions.SendNotificationToReceiver)
                .Name("Send Notification")
                .Type("checkbox");

            ConfigureModel(model => model.AdditionalOptions.ReceiverEmail)
                .Name("Receiver Email")
                .Type("textbox")
                .Pattern(@"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$");
            //.DependsOn(m => m.AdditionalOptions.SendNotificationToReceiver);

            ConfigureModel(model => model.AdditionalOptions.ReceiverMobile)
                .Name("Receiver Mobile")
                .Type("textbox")
                .Pattern(@"^\+?[0-9]{10,12}$");
            //.DependsOn(m => m.AdditionalOptions.SendNotificationToReceiver);

            ConfigureModel(model => model.AdditionalOptions.TransferMode)
                .Name("Transfer Mode")
                .Type("dropdown")
                .Required(true);
            //.Options(new[] { "NEFT", "RTGS", "IMPS" });

            ConfigureModel(model => model.AdditionalOptions.ScheduleType)
                .Name("Schedule Type")
                .Type("dropdown")
                .Required(true);
                //.Options(new[] { "One-time", "Recurring" });

            ConfigureModel(model => model.AdditionalOptions.FrequencyType)
                .Name("Frequency")
                .Type("dropdown");
                //.DependsOn(m => m.AdditionalOptions.ScheduleType == "Recurring")
                //.Options(new[] { "Daily", "Weekly", "Monthly" });
        }
    }
}
