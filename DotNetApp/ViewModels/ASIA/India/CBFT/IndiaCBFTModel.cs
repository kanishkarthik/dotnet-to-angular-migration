using DotNetApp.ViewModels.Base;
using System;

namespace Application.ViewModels.ASIA.India.CBFT
{
    public class IndiaCBFTModel : BaseAppModel
    {
        public PaymentDetailsSection PaymentDetails { get; set; }
        public BeneficiaryDetailsSection BeneficiaryDetails { get; set; }
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
