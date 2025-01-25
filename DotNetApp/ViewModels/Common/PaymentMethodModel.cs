namespace Application.ViewModels.Common
{
    public class PaymentMethodModel
    {
        public string AccountNumber { get; set; }
        public string AccountName { get; set; }
        public string Amount { get; set; }
        public string PaymentMethod { get; set; }
        public string PaymentCurrency { get; set; }
    }
}