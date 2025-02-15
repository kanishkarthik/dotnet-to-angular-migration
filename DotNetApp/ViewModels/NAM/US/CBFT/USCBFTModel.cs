using Application.ViewModels.Common;
using System;

namespace Application.ViewModels.NAM.US.CBFT
{
    public class USCBFTModel
    {
        public PaymentMethodSection PaymentMethod { get; set; }
        public USPaymentDetailsSection PaymentDetails { get; set; }
        public USBeneficiaryDetailsSection BeneficiaryDetails { get; set; }
    }

    public class USPaymentDetailsSection
    {
        public string TransactionReferenceNumber { get; set; }
        public DateTime ValueDate { get; set; }
        public bool IsUrgentPayment { get; set; }
        public string PaymentPurpose { get; set; }
        public string RemittanceInformation { get; set; }
        public string IntermediaryBankCode { get; set; }
        public bool HasIntermediaryBank { get; set; }
    }

    public class USBeneficiaryDetailsSection
    {
        public string BeneficiaryName { get; set; }
        public string AccountNumber { get; set; }
        public string BankName { get; set; }
        public string RoutingNumber { get; set; }
        public string BankAddress { get; set; }
        public string StateCode { get; set; }
        public string ZipCode { get; set; }
    }
}
