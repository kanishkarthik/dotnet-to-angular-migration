namespace Application.ViewModels.LandingPage
{
    public class LandingPagModel
    {
        public string BranchCode { get; set; }
        public string BranchName { get; set; }
        public string AccountNumber { get; set; }
        public string AccountName { get; set; }
        public string BankName { get; set; }

        public string PaymentCurrency { get; set; } = string.Empty;

        public string PaymentMethod { get; set; }
        public string PaymentType { get; set; }

        public decimal? Amount { get; set; }

    }
}