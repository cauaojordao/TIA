using System.ComponentModel.DataAnnotations;

namespace TIA.API.ViewModels
{
    public class RegisterViewModel
    {
        [Required]
        [EmailAddress]
        public string? Email { get; set; }

        [Required]
        [DataType(DataType.Password)]
        public string? Password { get; set; }

        [DataType(DataType.Password)]
        [Display(Name = "Confirm Your Password")]
        [Compare("Password", ErrorMessage = "The Passwords Don't Match")]
        public string? ConfirmPassword { get; set; }
    }
}
