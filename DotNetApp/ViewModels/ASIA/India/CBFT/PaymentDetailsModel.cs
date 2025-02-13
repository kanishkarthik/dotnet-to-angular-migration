namespace Application.ViewModels.ASIA.India.CBFT
{
    public class PaymentDetailsModel
    {
        public string TransactionReference { get; set; }
        public string ValueDate { get; set; }
        public string Currency { get; set; }
        public decimal Amount { get; set; }
        public string Purpose { get; set; }
        public string Remarks { get; set; }
        public bool IsConfidential { get; set; }
        public string ChargeBearer { get; set; }
    }
}
