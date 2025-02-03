namespace Application.ViewModels.ASIA.India.BKT
{
    public class PaymentDetailsModel
    {
        public string TranRefNo { get; set; }
        public string ValueDate { get; set; }
        public bool isConfidential { get; set; }
        public string EmailAddress { get; set; }

        public string TranTypeCode { get; set; }

        public string TranTypeDesc { get; set; }
    }
}