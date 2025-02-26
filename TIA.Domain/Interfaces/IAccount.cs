using TIA.Domain.Entities;

namespace TIA.Domain.Interfaces
{
    public interface IAccount
    {
        string Username { get; set; }
        string UserEmail { get; set; }
        string UserRole { get; set; }
        ICollection<AppFile>? Files { get; set; }
    }
}
