using TIA.Domain.Entities;

namespace TIA.Domain.Interfaces
{
    public interface IUser
    {
        string Username { get; set; }
        string Email { get; set; }
        ICollection<AppFile>? Files { get; set; }
    }
}
