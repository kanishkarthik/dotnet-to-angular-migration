using Application.ViewModels.Common;
using System;

namespace Application.ViewModels.ASIA.India.CBFT
{
    public class IndiaCBFTModel
    {
        public PaymentMethodSection PaymentMethod { get; set; }
        public PaymentDetailsSection PaymentDetails { get; set; }
        public BeneficiaryDetailsSection BeneficiaryDetails { get; set; }
    }

    public class PaymentMethodSection
    {
        public string AccountNumber { get; set; }
        public string PaymentCurrency { get; set; }
        public decimal Amount { get; set; }
        public string AccountName { get; set; }
        public string PaymentMethod { get; set; }
    }

    public class PaymentDetailsSection
    {
        public string TranRefNo { get; set; }
        public DateTime ValueDate { get; set; }
        public bool isUrgent { get; set; }
        public string PurposeCode { get; set; }
        public string PurposeDescription { get; set; }
        public string RemittanceInfo { get; set; }
    }

    public class BeneficiaryDetailsSection
    {
        public string BeneName { get; set; }
        public string BeneAcctNo { get; set; }
        public string BeneBank { get; set; }
        public string BeneBankCode { get; set; }
        public string BeneCountry { get; set; }
        public string AddrssLine1 { get; set; }
        public string AddrssLine2 { get; set; }
    }
}
