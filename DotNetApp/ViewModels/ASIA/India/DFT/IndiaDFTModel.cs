using DotNetApp.ViewModels.Base;
using System;
using System.ComponentModel.DataAnnotations;

namespace Application.ViewModels.ASIA.India.DFT
{
    public class IndiaDFTModel : BaseAppModel
    {
        public TransferDetailsSection TransferDetails { get; set; }
        public BeneficiarySection Beneficiary { get; set; }
        public AdditionalOptionsSection AdditionalOptions { get; set; }
    }

    public class TransferDetailsSection
    {
        public string TransferReferenceNumber { get; set; }
        public DateTime TransferDate { get; set; }
        public string TransferType { get; set; }
        public string PaymentPurpose { get; set; }
        public string Remarks { get; set; }
    }

    public class BeneficiarySection
    {
        [Required]
        public string BeneficiaryName { get; set; }
        [Required]
        public string BeneficiaryAccountNumber { get; set; }
        [Required]
        public string BeneficiaryBankName { get; set; }
        [Required]
        public string BeneficiaryIFSCCode { get; set; }
        public string BeneficiaryBankBranch { get; set; }
        public string BeneficiaryAddress { get; set; }
    }

    public class AdditionalOptionsSection
    {
        public bool IsUrgentPayment { get; set; }
        public bool SendNotificationToReceiver { get; set; }
        public string ReceiverEmail { get; set; }
        public string ReceiverMobile { get; set; }
        public string TransferMode { get; set; }  // NEFT/RTGS/IMPS
        public string ScheduleType { get; set; }  // One-time/Recurring
        public string FrequencyType { get; set; } // Daily/Weekly/Monthly
    }
}
